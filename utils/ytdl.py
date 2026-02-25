from __future__ import annotations

import asyncio
import functools
from dataclasses import dataclass

import os
from pathlib import Path

import discord
import yt_dlp

_COOKIES_FILE = os.getenv("COOKIES_FILE", "cookies.txt")
_cookies_opt = {"cookiefile": _COOKIES_FILE} if Path(_COOKIES_FILE).is_file() else {}

YTDL_SEARCH_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "extract_flat": "in_playlist",
    **_cookies_opt,
}

YTDL_EXTRACT_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    **_cookies_opt,
}

FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


@dataclass
class TrackInfo:
    title: str
    url: str
    webpage_url: str
    duration: int | None = None
    thumbnail: str | None = None
    uploader: str | None = None

    @property
    def duration_str(self) -> str:
        if self.duration is None:
            return "Unknown"
        m, s = divmod(self.duration, 60)
        h, m = divmod(m, 60)
        if h:
            return f"{h}:{m:02}:{s:02}"
        return f"{m}:{s:02}"


async def search_youtube(query: str) -> list[TrackInfo]:
    """Search YouTube and return top 5 results (metadata only, fast)."""
    loop = asyncio.get_running_loop()
    ytdl = yt_dlp.YoutubeDL(YTDL_SEARCH_OPTS)
    func = functools.partial(ytdl.extract_info, f"ytsearch5:{query}", download=False)
    data = await loop.run_in_executor(None, func)

    if not data or "entries" not in data:
        return []

    results = []
    for entry in data["entries"][:5]:
        if entry is None:
            continue
        webpage_url = entry.get("url", f"https://www.youtube.com/watch?v={entry.get('id', '')}")
        results.append(
            TrackInfo(
                title=entry.get("title", "Unknown"),
                url=webpage_url,
                webpage_url=webpage_url,
                duration=entry.get("duration"),
                thumbnail=entry.get("thumbnails", [{}])[0].get("url")
                if entry.get("thumbnails")
                else None,
                uploader=entry.get("uploader"),
            )
        )
    return results


async def extract_track(query: str) -> TrackInfo | None:
    """Extract full track info including stream URL. Use for direct URLs or re-extraction."""
    loop = asyncio.get_running_loop()
    ytdl = yt_dlp.YoutubeDL(YTDL_EXTRACT_OPTS)
    func = functools.partial(ytdl.extract_info, query, download=False)
    data = await loop.run_in_executor(None, func)

    if not data:
        return None

    # Handle playlists / search results that return entries
    if "entries" in data:
        data = data["entries"][0]
        if data is None:
            return None

    return TrackInfo(
        title=data.get("title", "Unknown"),
        url=data.get("url", ""),
        webpage_url=data.get("webpage_url", data.get("url", "")),
        duration=data.get("duration"),
        thumbnail=data.get("thumbnail"),
        uploader=data.get("uploader"),
    )


def create_audio_source(url: str, volume: float = 0.5) -> discord.PCMVolumeTransformer:
    """Create a Discord audio source from a stream URL."""
    source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTS)
    return discord.PCMVolumeTransformer(source, volume=volume)
