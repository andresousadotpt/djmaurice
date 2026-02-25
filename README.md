# DJMaurice - Discord Music Bot

A Discord music bot that plays YouTube audio in voice channels using slash commands.

> **WARNING:** This bot contains some absolutely unhinged commands. Use at your own risk. We are not responsible for any friendships destroyed, feelings hurt, or server chaos caused. You have been warned.

## Prerequisites

- Python 3.11+
- FFmpeg (`sudo pacman -S ffmpeg` / `sudo apt install ffmpeg`)
- A Discord bot token ([Discord Developer Portal](https://discord.com/developers/applications))

## Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure token
cp .env.example .env
# Edit .env and set your BOT_TOKEN and GUILD_ID

# Run
python bot.py
```

## Music Commands

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

## Fun Commands

| Command | Description |
|---------|-------------|
| `/speak <text> [lang]` | Bot joins voice and speaks text (supports multiple languages) |
| `/coinflip` | Flip a coin |
| `/roll [sides]` | Roll a dice |
| `/8ball <question>` | Ask the magic 8-ball |
| `/roast <user>` | Roast someone |
| `/fight <opponent>` | Fight another user |
| `/rate <thing>` | Rate anything 0-10 |
| `/choose <options>` | Pick from comma-separated options |
| `/pp [user]` | Measure pp size |
| `/wyr` | Would you rather... |
| `/ship <user1> <user2>` | Ship two users with compatibility score |

## Unhinged Commands

| Command | Description |
|---------|-------------|
| `/randomkick <channel_id>` | Randomly kick someone from a voice channel and shame them |
| `/hack <user>` | "Hack" a user with a fake terminal animation |
| `/roulette` | Russian roulette — 1/6 chance of 60s timeout |
| `/confess <user>` | Expose someone's "deepest secret" |
| `/nickname <user>` | Give someone a random cursed nickname |
| `/jumpscare` | Join voice and blast a loud noise |
| `/impersonate <user> <msg>` | Send a message pretending to be someone |
| `/ratio <user>` | Hit someone with the full ratio copypasta |
| `/scramble` | Scatter everyone in your voice channel to random channels |
| `/deafen <user> [seconds]` | Server deafen someone for up to 30 seconds |
| `/obituary <user>` | Write someone's obituary with autopsy report |
| `/wanted <user>` | Put a bounty on someone's head |
| `/trial <user> <crime>` | Put someone on trial with a jury verdict |
| `/dare` | Get a random dare |
| `/threat <user>` | Send a threatening message (legally a joke) |
| `/muteall [seconds]` | Server mute everyone in your voice channel |
| `/fakeping <user> [count]` | Ghost ping someone up to 5 times |
| `/kidnap <user>` | Drag someone into your voice channel |
| `/vckick <user>` | Kick someone from voice with a mocking message |
| `/copypasta <user>` | Generate a copypasta about someone |
| `/bounceball [times]` | Bounce everyone between two voice channels |

## Bot Permissions

When inviting the bot, ensure it has:
- Send Messages
- Manage Messages (for fakeping)
- Use Slash Commands
- Connect (voice)
- Speak (voice)
- Move Members (for kick/scramble/kidnap/bounceball)
- Mute Members (for muteall)
- Manage Nicknames (for nickname command)
- Moderate Members (for roulette timeout)
- Deafen Members (for deafen command)
