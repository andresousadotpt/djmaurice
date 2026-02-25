# DJMaurice - Discord Music Bot

A Discord music bot that plays YouTube audio in voice channels using slash commands.

## Prerequisites

- Python 3.11+
- FFmpeg (`sudo pacman -S ffmpeg` / `sudo apt install ffmpeg`)
- A Discord bot token ([Discord Developer Portal](https://discord.com/developers/applications))

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure token
cp .env.example .env
# Edit .env and set your BOT_TOKEN

# Run
python bot.py
```

## Commands

| Command | Description |
|---------|-------------|
| `/play <query>` | Play a YouTube URL or search for a track (shows dropdown) |
| `/stop` | Stop playback, clear queue, disconnect |
| `/skip` | Skip current track |
| `/queue` | Show current queue |
| `/pause` | Pause current track |
| `/resume` | Resume paused track |
| `/volume <0-100>` | Adjust playback volume |
| `/nowplaying` | Show current track info |
| `/shuffle` | Shuffle the queue |
| `/loop` | Cycle loop mode: off -> single -> queue -> off |

## Bot Permissions

When inviting the bot, ensure it has:
- Send Messages
- Use Slash Commands
- Connect (voice)
- Speak (voice)
