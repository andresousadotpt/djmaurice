from __future__ import annotations

import asyncio
import enum
import random
from dataclasses import dataclass, field

import discord
from discord import app_commands
from discord.ext import commands

from utils.ytdl import TrackInfo, create_audio_source, extract_track, search_youtube

INACTIVITY_TIMEOUT = 300  # 5 minutes


class LoopMode(enum.Enum):
    OFF = "off"
    SINGLE = "single"
    QUEUE = "queue"


@dataclass
class GuildQueue:
    tracks: list[TrackInfo] = field(default_factory=list)
    current: TrackInfo | None = None
    loop_mode: LoopMode = LoopMode.OFF
    volume: float = 0.5
    text_channel: discord.TextChannel | None = None
    _inactivity_task: asyncio.Task | None = field(default=None, repr=False)

    def clear(self) -> None:
        self.tracks.clear()
        self.current = None
        self._cancel_inactivity()

    def _cancel_inactivity(self) -> None:
        if self._inactivity_task and not self._inactivity_task.done():
            self._inactivity_task.cancel()
            self._inactivity_task = None


class SearchSelect(discord.ui.Select):
    def __init__(self, results: list[TrackInfo], cog: Music) -> None:
        self.results = results
        self.cog = cog
        options = []
        for i, track in enumerate(results):
            dur = track.duration_str if track.duration else "?"
            label = track.title[:100]
            options.append(
                discord.SelectOption(label=label, description=dur, value=str(i))
            )
        super().__init__(placeholder="Pick a track...", options=options)

    async def callback(self, interaction: discord.Interaction) -> None:
        idx = int(self.values[0])
        track = self.results[idx]
        await interaction.response.defer()

        guild_id = interaction.guild_id
        gq = self.cog._get_queue(guild_id)
        gq.text_channel = interaction.channel

        # Extract full track info
        full_track = await extract_track(track.webpage_url)
        if not full_track:
            await interaction.followup.send("Failed to extract track info.")
            return

        gq.tracks.append(full_track)
        if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
            await interaction.followup.send(f"**Queued:** {full_track.title}")
        else:
            await self.cog._play_next(interaction.guild)
            await interaction.followup.send(
                f"**Now playing:** {full_track.title}"
            )

        self.view.stop()


class SearchView(discord.ui.View):
    def __init__(self, results: list[TrackInfo], cog: Music) -> None:
        super().__init__(timeout=60)
        self.add_item(SearchSelect(results, cog))

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True


def _is_url(query: str) -> bool:
    return query.startswith(("http://", "https://"))


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._queues: dict[int, GuildQueue] = {}

    def _get_queue(self, guild_id: int) -> GuildQueue:
        if guild_id not in self._queues:
            self._queues[guild_id] = GuildQueue()
        return self._queues[guild_id]

    async def _ensure_voice(
        self, interaction: discord.Interaction
    ) -> discord.VoiceClient | None:
        """Join the user's voice channel if not already connected. Returns VoiceClient or None."""
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message(
                "You need to be in a voice channel.", ephemeral=True
            )
            return None

        vc = interaction.guild.voice_client
        target = interaction.user.voice.channel

        if vc is None:
            vc = await target.connect()
        elif vc.channel.id != target.id:
            await vc.move_to(target)

        return vc

    async def _play_next(self, guild: discord.Guild) -> None:
        gq = self._get_queue(guild.id)
        vc = guild.voice_client

        if vc is None:
            return

        gq._cancel_inactivity()

        # Handle loop modes
        if gq.loop_mode == LoopMode.SINGLE and gq.current:
            pass  # replay same track
        elif gq.loop_mode == LoopMode.QUEUE and gq.current:
            gq.tracks.append(gq.current)
            if gq.tracks:
                gq.current = gq.tracks.pop(0)
        else:
            if not gq.tracks:
                gq.current = None
                # Start inactivity timer
                gq._inactivity_task = asyncio.create_task(
                    self._inactivity_disconnect(guild)
                )
                return
            gq.current = gq.tracks.pop(0)

        # Re-extract stream URL (they expire)
        track = await extract_track(gq.current.webpage_url)
        if not track:
            if gq.text_channel:
                await gq.text_channel.send(
                    f"Failed to load **{gq.current.title}**, skipping..."
                )
            gq.current = None
            await self._play_next(guild)
            return

        gq.current = track
        source = create_audio_source(track.url, gq.volume)

        def after_play(error: Exception | None) -> None:
            if error:
                print(f"Player error: {error}")
            coro = self._play_next(guild)
            future = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                future.result(timeout=10)
            except Exception as e:
                print(f"Error in after callback: {e}")

        vc.play(source, after=after_play)

    async def _inactivity_disconnect(self, guild: discord.Guild) -> None:
        await asyncio.sleep(INACTIVITY_TIMEOUT)
        vc = guild.voice_client
        if vc and not vc.is_playing():
            gq = self._get_queue(guild.id)
            if gq.text_channel:
                await gq.text_channel.send(
                    "Disconnected due to inactivity."
                )
            gq.clear()
            await vc.disconnect()

    @app_commands.command(name="play", description="Play a YouTube URL or search for a track")
    @app_commands.describe(query="YouTube URL or search query")
    async def play(self, interaction: discord.Interaction, query: str) -> None:
        vc = await self._ensure_voice(interaction)
        if vc is None:
            return

        gq = self._get_queue(interaction.guild_id)
        gq.text_channel = interaction.channel

        if _is_url(query):
            await interaction.response.defer()
            track = await extract_track(query)
            if not track:
                await interaction.followup.send("Could not extract track from URL.")
                return

            gq.tracks.append(track)
            if vc.is_playing():
                await interaction.followup.send(f"**Queued:** {track.title}")
            else:
                await self._play_next(interaction.guild)
                await interaction.followup.send(
                    f"**Now playing:** {track.title}"
                )
        else:
            await interaction.response.defer()
            results = await search_youtube(query)
            if not results:
                await interaction.followup.send("No results found.")
                return

            view = SearchView(results, self)
            await interaction.followup.send(
                "Pick a track:", view=view
            )

    @app_commands.command(name="stop", description="Stop playback, clear queue, and disconnect")
    async def stop(self, interaction: discord.Interaction) -> None:
        vc = interaction.guild.voice_client
        if not vc:
            await interaction.response.send_message("Not connected.", ephemeral=True)
            return

        gq = self._get_queue(interaction.guild_id)
        gq.clear()
        vc.stop()
        await vc.disconnect()
        await interaction.response.send_message("Stopped and disconnected.")

    @app_commands.command(name="skip", description="Skip the current track")
    async def skip(self, interaction: discord.Interaction) -> None:
        vc = interaction.guild.voice_client
        if not vc or not vc.is_playing():
            await interaction.response.send_message("Nothing is playing.", ephemeral=True)
            return

        vc.stop()  # triggers after callback -> _play_next
        await interaction.response.send_message("Skipped.")

    @app_commands.command(name="queue", description="Show the current queue")
    async def queue(self, interaction: discord.Interaction) -> None:
        gq = self._get_queue(interaction.guild_id)

        if not gq.current and not gq.tracks:
            await interaction.response.send_message("Queue is empty.", ephemeral=True)
            return

        lines = []
        if gq.current:
            lines.append(f"**Now playing:** {gq.current.title} [{gq.current.duration_str}]")

        if gq.tracks:
            lines.append("")
            for i, track in enumerate(gq.tracks[:20], start=1):
                lines.append(f"`{i}.` {track.title} [{track.duration_str}]")
            if len(gq.tracks) > 20:
                lines.append(f"*...and {len(gq.tracks) - 20} more*")

        lines.append(f"\n**Loop:** {gq.loop_mode.value}")
        await interaction.response.send_message("\n".join(lines))

    @app_commands.command(name="pause", description="Pause the current track")
    async def pause(self, interaction: discord.Interaction) -> None:
        vc = interaction.guild.voice_client
        if not vc or not vc.is_playing():
            await interaction.response.send_message("Nothing is playing.", ephemeral=True)
            return

        vc.pause()
        await interaction.response.send_message("Paused.")

    @app_commands.command(name="resume", description="Resume the paused track")
    async def resume(self, interaction: discord.Interaction) -> None:
        vc = interaction.guild.voice_client
        if not vc or not vc.is_paused():
            await interaction.response.send_message("Nothing is paused.", ephemeral=True)
            return

        vc.resume()
        await interaction.response.send_message("Resumed.")

    @app_commands.command(name="volume", description="Set playback volume (0-100)")
    @app_commands.describe(level="Volume level from 0 to 100")
    async def volume(self, interaction: discord.Interaction, level: app_commands.Range[int, 0, 100]) -> None:
        gq = self._get_queue(interaction.guild_id)
        gq.volume = level / 100.0

        vc = interaction.guild.voice_client
        if vc and vc.source and isinstance(vc.source, discord.PCMVolumeTransformer):
            vc.source.volume = gq.volume

        await interaction.response.send_message(f"Volume set to **{level}%**.")

    @app_commands.command(name="nowplaying", description="Show info about the current track")
    async def nowplaying(self, interaction: discord.Interaction) -> None:
        gq = self._get_queue(interaction.guild_id)
        if not gq.current:
            await interaction.response.send_message("Nothing is playing.", ephemeral=True)
            return

        track = gq.current
        embed = discord.Embed(
            title="Now Playing",
            description=f"[{track.title}]({track.webpage_url})",
            color=discord.Color.blurple(),
        )
        if track.uploader:
            embed.add_field(name="Uploader", value=track.uploader, inline=True)
        embed.add_field(name="Duration", value=track.duration_str, inline=True)
        embed.add_field(name="Loop", value=gq.loop_mode.value, inline=True)
        if track.thumbnail:
            embed.set_thumbnail(url=track.thumbnail)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shuffle", description="Shuffle the queue")
    async def shuffle(self, interaction: discord.Interaction) -> None:
        gq = self._get_queue(interaction.guild_id)
        if len(gq.tracks) < 2:
            await interaction.response.send_message("Not enough tracks to shuffle.", ephemeral=True)
            return

        random.shuffle(gq.tracks)
        await interaction.response.send_message("Queue shuffled.")

    @app_commands.command(name="loop", description="Cycle loop mode: off -> single -> queue -> off")
    async def loop(self, interaction: discord.Interaction) -> None:
        gq = self._get_queue(interaction.guild_id)

        cycle = {
            LoopMode.OFF: LoopMode.SINGLE,
            LoopMode.SINGLE: LoopMode.QUEUE,
            LoopMode.QUEUE: LoopMode.OFF,
        }
        gq.loop_mode = cycle[gq.loop_mode]
        await interaction.response.send_message(f"Loop mode: **{gq.loop_mode.value}**")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Music(bot))
