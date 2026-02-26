from __future__ import annotations

import asyncio
import functools
import logging
import os
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import discord
import yt_dlp

log = logging.getLogger(__name__)

_POT_HOST = os.getenv("POT_PROVIDER_HOST")


def _check_pot_provider() -> bool:
    """Check if the PO token provider is reachable."""
    if not _POT_HOST:
        return False
    try:
        urllib.request.urlopen(_POT_HOST, timeout=5)
        return True
    except urllib.error.HTTPError:
        # 404 etc on root path is fine — server is up, just no root handler
        return True
    except Exception as e:
        log.error("PO token provider at %s is NOT reachable: %s", _POT_HOST, e)
        return False


def _auth_opts() -> dict:
    """Build auth options. PO token provider only (no expired cookies)."""
    opts: dict = {}
    if _POT_HOST:
        reachable = _check_pot_provider()
        if reachable:
            log.info("PO token provider at %s is reachable", _POT_HOST)
        opts["extractor_args"] = {
            "youtubepot-bgutilhttp": {"base_url": [_POT_HOST]},
        }
    else:
        log.warning("POT_PROVIDER_HOST not set — PO token provider disabled")
        log.warning("YouTube will likely block requests")
    return opts


_auth = _auth_opts()

_COMMON_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "verbose": bool(os.getenv("YTDL_VERBOSE")),
    "js_runtimes": {"node": {}, "deno": {}},
    **_auth,
}

YTDL_SEARCH_OPTS = {
    **_COMMON_OPTS,
    "extract_flat": "in_playlist",
}

YTDL_EXTRACT_OPTS = {
    **_COMMON_OPTS,
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
