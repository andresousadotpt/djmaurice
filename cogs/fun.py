from __future__ import annotations

import asyncio
import io
import random
import tempfile
from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands
from gtts import gTTS

import os

ALLOWED_USER_ID = 208764438696689665
TTS_LANG = os.getenv("TTS_LANG", "en")
SHAME_CHANNEL_ID = 794497017019105290

MOCK_MESSAGES = [
    "got absolutely YEETED from the voice channel",
    "was randomly chosen by fate... and fate said GET OUT",
    "didn't see it coming. Nobody did. Except the bot.",
    "has been banished to the shadow realm (lobby)",
    "was the unlucky one. Better luck next time.",
    "just got kicked for no reason whatsoever. Love it.",
    "tried to vibe but the bot said no",
    "was sacrificed for the greater good",
]

EIGHT_BALL_RESPONSES = [
    "It is certain.", "It is decidedly so.", "Without a doubt.",
    "Yes, definitely.", "You may rely on it.", "As I see it, yes.",
    "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
    "Reply hazy, try again.", "Ask again later.",
    "Better not tell you now.", "Cannot predict now.",
    "Concentrate and ask again.", "Don't count on it.",
    "My reply is no.", "My sources say no.",
    "Outlook not so good.", "Very doubtful.",
]

ROAST_MESSAGES = [
    "You're the reason God created the middle finger.",
    "If you were any more inbred, you'd be a sandwich.",
    "You bring everyone so much joy... when you leave.",
    "I'd explain it to you, but I left my crayons at home.",
    "You're like a cloud. When you disappear, it's a beautiful day.",
    "You're not stupid; you just have bad luck thinking.",
    "If brains were dynamite, you wouldn't have enough to blow your nose.",
    "You're proof that even evolution makes mistakes.",
    "I'd roast you, but I don't want to set off the smoke detector.",
    "You're the human equivalent of a participation trophy.",
    "Your secrets are always safe with me. I never even listen when you talk.",
    "You're like a software update. Whenever I see you, I think 'not now'.",
]

FIGHT_MOVES = [
    "{winner} landed a devastating uppercut on {loser}!",
    "{winner} hit {loser} with a flying roundhouse kick!",
    "{winner} suplexed {loser} into another dimension!",
    "{winner} absolutely demolished {loser} with a chair!",
    "{loser} tried to run but {winner} caught them!",
    "{winner} used {loser} as a mop and cleaned the floor!",
    "{loser} slipped on a banana peel and {winner} won by default!",
    "{winner} stared at {loser} so hard they fainted!",
    "{winner} sent {loser} to the shadow realm!",
]

FAKE_HACK_LINES = [
    "Connecting to mainframe...",
    "Bypassing firewall... [OK]",
    "Downloading browsing history... 23%... 58%... 91%...",
    "Extracting saved passwords...",
    "Accessing webcam feed...",
    "Uploading data to pastebin...",
    "Installing keylogger... [OK]",
    "Reading DMs... oh no...",
    "Found 847 unread emails...",
    "Decrypting files... [OK]",
    "IP address located: 127.0.0.1",
    "Installing Fortnite... just kidding",
    "Deleting System32...",
    "Done. All data has been sold on the dark web.",
]

SHIP_RATINGS = [
    (0, 20, "Absolutely not. Restrain yourselves."),
    (21, 40, "Hmm... I don't see it."),
    (41, 60, "There's something there... maybe?"),
    (61, 80, "I ship it. Lowkey."),
    (81, 95, "THEY'RE PERFECT FOR EACH OTHER."),
    (96, 100, "GET MARRIED ALREADY."),
]

WOULD_YOU_RATHER = [
    ("always speak in caps lock", "never use punctuation again"),
    ("have your search history made public", "never use the internet again"),
    ("fight 100 duck-sized horses", "fight 1 horse-sized duck"),
    ("only communicate through memes", "only communicate through song lyrics"),
    ("have no elbows", "have no knees"),
    ("always be 10 minutes late", "always be 2 hours early"),
    ("have fingers as long as your legs", "legs as long as your fingers"),
    ("smell like onions forever", "cry every time you see a dog"),
    ("only eat pizza for every meal", "never eat pizza again"),
    ("accidentally like a 5-year-old post", "send a text to the wrong person every day"),
    ("fight your dad at full strength", "fight your mom who knows martial arts"),
    ("have hands for feet", "feet for hands"),
    ("be able to fly but only 2 feet off the ground", "be invisible but only when nobody is looking"),
    ("always have a song stuck in your head", "always have an itch you can't reach"),
]

CONFESS_PREFIXES = [
    "{user} secretly",
    "Breaking news: {user}",
    "Sources confirm that {user}",
    "My inside sources tell me {user}",
    "Leaked documents reveal {user}",
]

CONFESS_ACTIONS = [
    "still sleeps with a nightlight on.",
    "has 47 tabs open right now. All of them are memes.",
    "once googled 'how to be cool' unironically.",
    "cried during a Disney movie last week.",
    "talks to their pets in a baby voice.",
    "has a secret TikTok account with 3 followers.",
    "practices their Oscar acceptance speech in the shower.",
    "once waved back at someone who wasn't waving at them.",
    "has never finished a single book.",
    "still doesn't know the difference between there/their/they're.",
    "ate cereal for dinner 4 times this week.",
    "has a playlist called 'songs to cry to'.",
    "screenshots conversations to send to their friends.",
    "googles how to spell 'definitely' every single time.",
    "pretends to text someone when walking alone.",
]

NICKNAME_POOL = [
    "certified clown", "big stinky", "Discord's Finest Loser",
    "bottom of the food chain", "professional idiot", "cringe lord",
    "NPC #4827", "error 404: braincells not found", "the weakest link",
    "uninstall yourself", "L + ratio", "copium addict",
    "skill issue", "touch grass", "a disappointment",
    "fortnite kid", "ur mom's favorite", "reddit moderator",
]

OBITUARY_CAUSES = [
    "died from cringe after reading their own messages.",
    "was found lifeless after losing an argument on Discord.",
    "passed away peacefully while waiting for someone to play with them.",
    "tragically died after accidentally sending a message to the wrong channel.",
    "was eliminated by natural selection after their last hot take.",
    "died doing what they loved: being wrong.",
    "spontaneously combusted after someone said 'skill issue'.",
    "was found unresponsive after their WiFi disconnected mid-ranked game.",
    "died of embarrassment. We all saw what they posted.",
    "was last seen typing... and was never heard from again.",
]

WANTED_CRIMES = [
    "being too annoying in voice chat",
    "using light mode",
    "posting cringe",
    "being down bad in DMs",
    "sending unsolicited game invites",
    "being AFK in voice for 6 hours",
    "spamming @everyone",
    "having a trash music taste",
    "using too many emojis unironically",
    "being a Discord mod",
    "having 0 bitches",
    "existing",
    "committing war crimes in Minecraft",
    "breathing too loud on mic",
]

TRIAL_VERDICTS = [
    "GUILTY of being a menace to society. Sentenced to 1000 years of mute.",
    "NOT GUILTY. The court finds {user} to be only slightly insufferable.",
    "GUILTY. The evidence was overwhelming. Everyone saw what you did.",
    "GUILTY by unanimous decision. Even your own lawyer voted against you.",
    "NOT GUILTY by reason of insanity. {user} is clearly not well.",
    "MISTRIAL. The judge ragequit after seeing the evidence.",
    "GUILTY. Sentenced to change their profile picture to a minion forever.",
    "NOT GUILTY. But the court recommends therapy.",
    "GUILTY on all counts. {user} is hereby banned from having opinions.",
    "GUILTY. The jury didn't even need to deliberate. It took 3 seconds.",
]

DARE_MESSAGES = [
    "Change your nickname to 'I love {other}' for 10 minutes.",
    "Send 'I'm a furry and I'm proud' in general chat.",
    "Voice chat using only a Mickey Mouse voice for 5 minutes.",
    "Let someone else send a message from your account.",
    "Set your status to 'Looking for a Discord girlfriend' for 1 hour.",
    "Compliment everyone in the voice channel sincerely.",
    "Type with your elbows for the next 3 messages.",
    "Admit your most embarrassing gaming moment.",
    "Send your last saved photo (no cheating).",
    "Let the person below you change your nickname.",
    "Speak in a British accent for 10 minutes.",
    "Only communicate through song lyrics for 5 minutes.",
    "Post your screen time stats.",
    "Confess which server member you'd trust least with your phone.",
]

AUTOPSY_REPORTS = [
    "Brain: smooth. Completely smooth. Not a single wrinkle.",
    "Stomach contents: energy drinks and pure copium.",
    "Last words: 'It's not lag, my internet is fine.'",
    "Cause of death: emotional damage.",
    "Note from coroner: 'I've never seen anyone this down bad.'",
    "Blood type: L negative.",
    "Time of death: the moment they joined this server.",
]

THREAT_MESSAGES = [
    "I will mass ping you at 3 AM.",
    "Your IP address is 192.168.1.1. Wait... that's mine.",
    "I will find your Roblox account.",
    "I'm in your walls. Just kidding. Unless?",
    "I will leak your Spotify Wrapped. It's embarrassing.",
    "Your search history is interesting. Very interesting.",
    "I'm telling your mom what you said in voice chat.",
    "I will sign you up for every newsletter on the internet.",
    "Your Discord status says 'online' but your grades say 'offline'.",
    "I will replace all your Spotify playlists with Baby Shark remixes.",
]


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="randomkick", description="Randomly kick someone from a voice channel")
    @app_commands.describe(channel_id="The voice channel ID")
    async def randomkick(self, interaction: discord.Interaction, channel_id: str) -> None:
        channel = self.bot.get_channel(int(channel_id))
        if not channel or not isinstance(channel, discord.VoiceChannel):
            await interaction.response.send_message("Invalid voice channel ID.", ephemeral=True)
            return

        members = [m for m in channel.members if not m.bot]
        if not members:
            await interaction.response.send_message("No users in that voice channel.", ephemeral=True)
            return

        victim = random.choice(members)
        await interaction.response.defer()

        await victim.move_to(None)

        mock = random.choice(MOCK_MESSAGES)
        await interaction.followup.send(f"Kicked **{victim.display_name}** from {channel.name}.")

        shame_channel = self.bot.get_channel(SHAME_CHANNEL_ID)
        if shame_channel:
            await shame_channel.send(f"{victim.mention} {mock}")

    @app_commands.command(name="speak", description="Bot joins your voice channel and speaks the text")
    @app_commands.describe(text="The text to speak", lang="Language (default from env)")
    @app_commands.choices(lang=[
        app_commands.Choice(name="English", value="en"),
        app_commands.Choice(name="Portuguese", value="pt"),
        app_commands.Choice(name="Spanish", value="es"),
        app_commands.Choice(name="French", value="fr"),
        app_commands.Choice(name="German", value="de"),
        app_commands.Choice(name="Italian", value="it"),
        app_commands.Choice(name="Japanese", value="ja"),
        app_commands.Choice(name="Korean", value="ko"),
        app_commands.Choice(name="Russian", value="ru"),
        app_commands.Choice(name="Chinese", value="zh-CN"),
    ])
    async def speak(self, interaction: discord.Interaction, text: str, lang: str | None = None) -> None:
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("You need to be in a voice channel.", ephemeral=True)
            return

        await interaction.response.defer()

        # Generate TTS audio in executor to avoid blocking
        loop = asyncio.get_running_loop()
        mp3_buffer = io.BytesIO()
        tts = gTTS(text=text, lang=lang or TTS_LANG)
        await loop.run_in_executor(None, tts.write_to_fp, mp3_buffer)
        mp3_buffer.seek(0)

        # Write to temp file (FFmpeg needs a seekable file)
        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tmp.write(mp3_buffer.read())
        tmp.close()

        # Connect to voice
        target = interaction.user.voice.channel
        vc = interaction.guild.voice_client
        if vc is None:
            vc = await target.connect()
        elif vc.channel.id != target.id:
            await vc.move_to(target)

        # Stop any current playback
        if vc.is_playing():
            vc.stop()

        done = asyncio.Event()

        def after_play(error):
            import os
            os.unlink(tmp.name)
            self.bot.loop.call_soon_threadsafe(done.set)

        vc.play(discord.FFmpegPCMAudio(tmp.name), after=after_play)
        await interaction.followup.send(f'Speaking: "{text}"')
        await done.wait()

    @app_commands.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction) -> None:
        result = random.choice(["Heads", "Tails"])
        await interaction.response.send_message(f"**{result}!**")

    @app_commands.command(name="roll", description="Roll a dice")
    @app_commands.describe(sides="Number of sides (default 6)")
    async def roll(self, interaction: discord.Interaction, sides: int = 6) -> None:
        if sides < 2:
            await interaction.response.send_message("Dice needs at least 2 sides.", ephemeral=True)
            return
        result = random.randint(1, sides)
        await interaction.response.send_message(f"**{result}** (d{sides})")

    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question")
    @app_commands.describe(question="Your yes/no question")
    async def eight_ball(self, interaction: discord.Interaction, question: str) -> None:
        answer = random.choice(EIGHT_BALL_RESPONSES)
        await interaction.response.send_message(f"> {question}\n**{answer}**")

    @app_commands.command(name="roast", description="Roast someone")
    @app_commands.describe(user="The user to roast")
    async def roast(self, interaction: discord.Interaction, user: discord.Member) -> None:
        roast = random.choice(ROAST_MESSAGES)
        await interaction.response.send_message(f"{user.mention} {roast}")

    @app_commands.command(name="fight", description="Fight another user")
    @app_commands.describe(opponent="Who do you want to fight?")
    async def fight(self, interaction: discord.Interaction, opponent: discord.Member) -> None:
        if opponent.id == interaction.user.id:
            await interaction.response.send_message("You can't fight yourself... or can you?", ephemeral=True)
            return
        if opponent.bot:
            await interaction.response.send_message(f"**{opponent.display_name}** dodged effortlessly. You can't fight a bot.")
            return

        winner, loser = random.choice([
            (interaction.user, opponent),
            (opponent, interaction.user),
        ])
        move = random.choice(FIGHT_MOVES).format(winner=winner.display_name, loser=loser.display_name)
        damage = random.randint(50, 999)
        await interaction.response.send_message(f"{move}\n**{damage} damage!** {winner.mention} wins!")

    @app_commands.command(name="rate", description="Rate anything 0-10")
    @app_commands.describe(thing="What should I rate?")
    async def rate(self, interaction: discord.Interaction, thing: str) -> None:
        score = random.randint(0, 10)
        bars = "+" * score + "-" * (10 - score)
        await interaction.response.send_message(f"I rate **{thing}** a **{score}/10**\n`[{bars}]`")

    @app_commands.command(name="roulette", description="Russian roulette - get timed out for 60s if you lose")
    async def roulette(self, interaction: discord.Interaction) -> None:
        chamber = random.randint(1, 6)
        if chamber == 1:
            try:
                await interaction.user.timeout(
                    discord.utils.utcnow() + timedelta(seconds=60)
                )
                await interaction.response.send_message(f"**BANG!** {interaction.user.mention} got timed out for 60 seconds!")
            except discord.Forbidden:
                await interaction.response.send_message(f"**BANG!** {interaction.user.mention} got lucky — I can't time them out.")
        else:
            await interaction.response.send_message(f"*click*... {interaction.user.mention} survived! ({chamber}/6)")

    @app_commands.command(name="choose", description="Let the bot choose for you")
    @app_commands.describe(choices="Comma-separated options (e.g. pizza, sushi, burger)")
    async def choose(self, interaction: discord.Interaction, choices: str) -> None:
        options = [c.strip() for c in choices.split(",") if c.strip()]
        if len(options) < 2:
            await interaction.response.send_message("Give me at least 2 options separated by commas.", ephemeral=True)
            return
        pick = random.choice(options)
        await interaction.response.send_message(f"I choose... **{pick}**!")

    @app_commands.command(name="pp", description="Measure someone's pp size")
    @app_commands.describe(user="Whose pp to measure (default: yourself)")
    async def pp(self, interaction: discord.Interaction, user: discord.Member | None = None) -> None:
        target = user or interaction.user
        size = random.randint(1, 12)
        shaft = "=" * size
        await interaction.response.send_message(f"{target.mention}'s pp\n8{shaft}D")

    @app_commands.command(name="hack", description="Hack a user (totally real)")
    @app_commands.describe(user="The victim")
    async def hack(self, interaction: discord.Interaction, user: discord.Member) -> None:
        await interaction.response.defer()
        lines = random.sample(FAKE_HACK_LINES, k=min(6, len(FAKE_HACK_LINES)))
        msg = await interaction.followup.send(f"**Hacking {user.display_name}...**\n```\n{lines[0]}\n```")
        for line in lines[1:]:
            await asyncio.sleep(1.5)
            current = msg.content.replace("```", "").split("\n")
            progress = "\n".join(current[1:]) + f"\n{line}"
            await msg.edit(content=f"**Hacking {user.display_name}...**\n```\n{progress}\n```")
        await asyncio.sleep(1)
        await msg.edit(content=f"**{user.mention} has been completely hacked.** All their data now belongs to me.")

    @app_commands.command(name="ship", description="Ship two users and get a compatibility score")
    @app_commands.describe(user1="First person", user2="Second person")
    async def ship(self, interaction: discord.Interaction, user1: discord.Member, user2: discord.Member) -> None:
        # Deterministic score based on user IDs so it's consistent
        seed = user1.id + user2.id
        rng = random.Random(seed)
        score = rng.randint(0, 100)
        bar_filled = round(score / 10)
        bar = "+" * bar_filled + "-" * (10 - bar_filled)
        verdict = ""
        for low, high, msg in SHIP_RATINGS:
            if low <= score <= high:
                verdict = msg
                break
        name = user1.display_name[:len(user1.display_name)//2] + user2.display_name[len(user2.display_name)//2:]
        await interaction.response.send_message(
            f"**{user1.display_name}** x **{user2.display_name}**\n"
            f"Ship name: **{name}**\n"
            f"`[{bar}]` **{score}%**\n"
            f"{verdict}"
        )

    @app_commands.command(name="wyr", description="Would you rather...")
    async def wyr(self, interaction: discord.Interaction) -> None:
        a, b = random.choice(WOULD_YOU_RATHER)
        await interaction.response.send_message(f"**Would you rather...**\n\nA) {a}\n\nor\n\nB) {b}")

    @app_commands.command(name="confess", description="Expose someone's deepest secret (totally real)")
    @app_commands.describe(user="Who to expose")
    async def confess(self, interaction: discord.Interaction, user: discord.Member) -> None:
        prefix = random.choice(CONFESS_PREFIXES).format(user=user.display_name)
        action = random.choice(CONFESS_ACTIONS)
        await interaction.response.send_message(f"{prefix} {action}")

    @app_commands.command(name="nickname", description="Give someone a random cursed nickname")
    @app_commands.describe(user="The victim")
    async def nickname(self, interaction: discord.Interaction, user: discord.Member) -> None:
        nick = random.choice(NICKNAME_POOL)
        try:
            await user.edit(nick=nick)
            await interaction.response.send_message(f"{user.mention} is now known as **{nick}**")
        except discord.Forbidden:
            await interaction.response.send_message(f"I can't change their nickname, but they should be called **{nick}**")

    @app_commands.command(name="jumpscare", description="Join voice and blast a loud noise")
    async def jumpscare(self, interaction: discord.Interaction) -> None:
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("You need to be in a voice channel.", ephemeral=True)
            return

        await interaction.response.defer()

        # Generate a loud beep TTS
        loop = asyncio.get_running_loop()
        mp3_buffer = io.BytesIO()
        tts = gTTS(text="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", lang="en")
        await loop.run_in_executor(None, tts.write_to_fp, mp3_buffer)
        mp3_buffer.seek(0)

        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tmp.write(mp3_buffer.read())
        tmp.close()

        target = interaction.user.voice.channel
        vc = interaction.guild.voice_client
        if vc is None:
            vc = await target.connect()
        elif vc.channel.id != target.id:
            await vc.move_to(target)

        if vc.is_playing():
            vc.stop()

        done = asyncio.Event()

        def after_play(error):
            os.unlink(tmp.name)
            self.bot.loop.call_soon_threadsafe(done.set)

        # Max volume
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(tmp.name), volume=2.0)
        vc.play(source, after=after_play)
        await interaction.followup.send("BOO!")
        await done.wait()

    @app_commands.command(name="impersonate", description="Send a message pretending to be someone")
    @app_commands.describe(user="Who to impersonate", message="What they 'said'")
    async def impersonate(self, interaction: discord.Interaction, user: discord.Member, message: str) -> None:
        embed = discord.Embed(description=message, color=discord.Color.random())
        embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
        embed.set_footer(text=f"(impersonated by {interaction.user.display_name})")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ratio", description="Ratio someone")
    @app_commands.describe(user="Who to ratio")
    async def ratio(self, interaction: discord.Interaction, user: discord.Member) -> None:
        await interaction.response.send_message(
            f"{user.mention}\n\nL + ratio + you fell off + cope + seethe + mald + "
            f"no bitches + touch grass + skill issue + cry about it + "
            f"stay mad + git gud + counter ratio + you're white + "
            f"the audacity + nerd + let's see your stats"
        )

    @app_commands.command(name="scramble", description="Move everyone in your voice channel to random channels")
    async def scramble(self, interaction: discord.Interaction) -> None:
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("You need to be in a voice channel.", ephemeral=True)
            return

        source = interaction.user.voice.channel
        members = [m for m in source.members if not m.bot]
        if len(members) < 2:
            await interaction.response.send_message("Need at least 2 people to scramble.", ephemeral=True)
            return

        voice_channels = [c for c in interaction.guild.voice_channels if c.id != source.id and c.permissions_for(interaction.guild.me).move_members]
        if not voice_channels:
            await interaction.response.send_message("No other voice channels to scatter people to.", ephemeral=True)
            return

        await interaction.response.defer()
        for member in members:
            target = random.choice(voice_channels)
            try:
                await member.move_to(target)
            except discord.Forbidden:
                pass
        await interaction.followup.send(f"Scattered {len(members)} people across the server!")

    @app_commands.command(name="deafen", description="Server deafen someone for a few seconds")
    @app_commands.describe(user="The victim", seconds="How long (max 30)")
    async def deafen(self, interaction: discord.Interaction, user: discord.Member, seconds: app_commands.Range[int, 1, 30] = 10) -> None:
        if not user.voice:
            await interaction.response.send_message("They're not in a voice channel.", ephemeral=True)
            return

        try:
            await user.edit(deafen=True)
            await interaction.response.send_message(f"{user.mention} has been deafened for {seconds} seconds!")
            await asyncio.sleep(seconds)
            await user.edit(deafen=False)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to do that.", ephemeral=True)

    @app_commands.command(name="obituary", description="Write someone's obituary")
    @app_commands.describe(user="The deceased")
    async def obituary(self, interaction: discord.Interaction, user: discord.Member) -> None:
        cause = random.choice(OBITUARY_CAUSES)
        report = random.choice(AUTOPSY_REPORTS)
        years = random.randint(1, 99)
        embed = discord.Embed(
            title=f"REST IN PEACE - {user.display_name}",
            description=(
                f"{user.mention} {cause}\n\n"
                f"They were {years} years old (mentally).\n\n"
                f"**Autopsy Report:**\n{report}\n\n"
                f"*Press F to pay respects.*"
            ),
            color=discord.Color.dark_grey(),
        )
        if user.display_avatar:
            embed.set_thumbnail(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="wanted", description="Put a bounty on someone's head")
    @app_commands.describe(user="The criminal")
    async def wanted(self, interaction: discord.Interaction, user: discord.Member) -> None:
        crime = random.choice(WANTED_CRIMES)
        bounty = random.randint(1, 1000000)
        embed = discord.Embed(
            title="WANTED DEAD OR ALIVE",
            description=(
                f"**{user.display_name}**\n\n"
                f"**Crime:** {crime}\n"
                f"**Bounty:** ${bounty:,}\n"
                f"**Danger Level:** {'*' * random.randint(1, 5)}/{'*' * 5}\n\n"
                f"*If you see this individual, report immediately.*"
            ),
            color=discord.Color.red(),
        )
        if user.display_avatar:
            embed.set_thumbnail(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="trial", description="Put someone on trial")
    @app_commands.describe(user="The defendant", crime="What they're accused of")
    async def trial(self, interaction: discord.Interaction, user: discord.Member, crime: str) -> None:
        await interaction.response.defer()
        msg = await interaction.followup.send(
            f"**THE COURT OF DISCORD**\n\n"
            f"**{user.display_name}** stands accused of: *{crime}*\n\n"
            f"The jury is deliberating..."
        )
        await asyncio.sleep(3)
        verdict = random.choice(TRIAL_VERDICTS).format(user=user.display_name)
        await msg.edit(
            content=(
                f"**THE COURT OF DISCORD**\n\n"
                f"**{user.display_name}** stands accused of: *{crime}*\n\n"
                f"**VERDICT:** {verdict}"
            )
        )

    @app_commands.command(name="dare", description="Get a random dare")
    async def dare(self, interaction: discord.Interaction) -> None:
        # Pick a random member to reference in the dare
        members = [m for m in interaction.guild.members if not m.bot and m.id != interaction.user.id]
        other = random.choice(members).display_name if members else "someone"
        d = random.choice(DARE_MESSAGES).format(other=other)
        await interaction.response.send_message(f"**{interaction.user.display_name}, I dare you to:**\n\n{d}")

    @app_commands.command(name="threat", description="Send a threatening message to someone (for legal reasons, this is a joke)")
    @app_commands.describe(user="Who to threaten")
    async def threat(self, interaction: discord.Interaction, user: discord.Member) -> None:
        msg = random.choice(THREAT_MESSAGES)
        await interaction.response.send_message(f"{user.mention} {msg}")

    @app_commands.command(name="muteall", description="Server mute everyone in your voice channel for a few seconds")
    @app_commands.describe(seconds="How long (max 30)")
    async def muteall(self, interaction: discord.Interaction, seconds: app_commands.Range[int, 1, 30] = 10) -> None:
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("You need to be in a voice channel.", ephemeral=True)
            return

        channel = interaction.user.voice.channel
        members = [m for m in channel.members if not m.bot]
        if len(members) < 2:
            await interaction.response.send_message("Need at least 2 people.", ephemeral=True)
            return

        await interaction.response.defer()
        muted = []
        for member in members:
            try:
                await member.edit(mute=True)
                muted.append(member)
            except discord.Forbidden:
                pass

        await interaction.followup.send(f"Everyone shut up for {seconds} seconds! ({len(muted)} muted)")
        await asyncio.sleep(seconds)
        for member in muted:
            try:
                await member.edit(mute=False)
            except discord.Forbidden:
                pass

    @app_commands.command(name="fakeping", description="Ping someone with a fake message notification")
    @app_commands.describe(user="Who to fake ping", count="How many times (max 5)")
    async def fakeping(self, interaction: discord.Interaction, user: discord.Member, count: app_commands.Range[int, 1, 5] = 3) -> None:
        await interaction.response.send_message(f"Pinging {user.display_name}...", ephemeral=True)
        for _ in range(count):
            msg = await interaction.channel.send(f"{user.mention}")
            await msg.delete()
            await asyncio.sleep(0.5)

    @app_commands.command(name="kidnap", description="Drag someone into your voice channel")
    @app_commands.describe(user="Who to kidnap")
    async def kidnap(self, interaction: discord.Interaction, user: discord.Member) -> None:
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("You need to be in a voice channel.", ephemeral=True)
            return
        if not user.voice:
            await interaction.response.send_message("They're not in any voice channel.", ephemeral=True)
            return

        target = interaction.user.voice.channel
        try:
            await user.move_to(target)
            await interaction.response.send_message(f"{user.mention} has been kidnapped and dragged to **{target.name}**!")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to move them.", ephemeral=True)

    @app_commands.command(name="vckick", description="Kick someone from voice chat")
    @app_commands.describe(user="Who to kick")
    async def vckick(self, interaction: discord.Interaction, user: discord.Member) -> None:
        if not user.voice:
            await interaction.response.send_message("They're not in a voice channel.", ephemeral=True)
            return
        try:
            await user.move_to(None)
            mock = random.choice(MOCK_MESSAGES)
            await interaction.response.send_message(f"{user.mention} {mock}")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to do that.", ephemeral=True)

    @app_commands.command(name="copypasta", description="Generate a copypasta about someone")
    @app_commands.describe(user="The subject")
    async def copypasta(self, interaction: discord.Interaction, user: discord.Member) -> None:
        templates = [
            (
                f"I just saw {user.display_name} at the grocery store. I told them how cool it was to meet them "
                f"in person, but I didn't want to be a douche and bother them and ask them for photos or anything. "
                f"They said, 'Oh, like you're doing now?' I was taken aback, and all I could say was 'Huh?' "
                f"but they kept cutting me off and going 'huh? huh? huh?' and closing their hand shut in front "
                f"of my face."
            ),
            (
                f"What the heck did you just say about {user.display_name}, you little noob? I'll have you "
                f"know they graduated top of their class in Discord moderation, and they've been involved in "
                f"numerous secret raids on rival servers, and they have over 300 confirmed bans."
            ),
            (
                f"Guys, I'm literally shaking and crying right now. {user.display_name} just DMed me and "
                f"said 'lol'. What does this mean? Are they into me? I've been analyzing this message for "
                f"3 hours. My palms are sweaty. Mom's spaghetti."
            ),
            (
                f"BREAKING: {user.display_name} has been caught speedrunning being cringe. Their time of "
                f"0.3 seconds has set a new world record, beating the previous holder by a significant margin. "
                f"The speedrunning community is in shambles."
            ),
            (
                f"Dear {user.display_name}, you claim to be a gamer, yet you have touched grass at least "
                f"once this week. Curious. Turning Point Discord."
            ),
            (
                f"I used to be a normal person. Then {user.display_name} joined the server. Now I have "
                f"trust issues, a caffeine addiction, and an irrational fear of Discord notifications. "
                f"This is their fault. Everything is their fault."
            ),
        ]
        pasta = random.choice(templates)
        await interaction.response.send_message(pasta)

    @app_commands.command(name="bounceball", description="Bounce everyone between two voice channels rapidly")
    @app_commands.describe(times="Number of bounces (max 5)")
    async def bounceball(self, interaction: discord.Interaction, times: app_commands.Range[int, 1, 5] = 3) -> None:
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("You need to be in a voice channel.", ephemeral=True)
            return

        source = interaction.user.voice.channel
        voice_channels = [c for c in interaction.guild.voice_channels if c.id != source.id and c.permissions_for(interaction.guild.me).move_members]
        if not voice_channels:
            await interaction.response.send_message("No other voice channels available.", ephemeral=True)
            return

        target = random.choice(voice_channels)
        members = [m for m in source.members if not m.bot]
        if not members:
            await interaction.response.send_message("No one to bounce.", ephemeral=True)
            return

        await interaction.response.defer()
        for _ in range(times):
            for member in members:
                try:
                    await member.move_to(target)
                except discord.Forbidden:
                    pass
            await asyncio.sleep(1)
            for member in members:
                try:
                    await member.move_to(source)
                except discord.Forbidden:
                    pass
            await asyncio.sleep(1)
        await interaction.followup.send(f"Bounced {len(members)} people {times} times between **{source.name}** and **{target.name}**!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
