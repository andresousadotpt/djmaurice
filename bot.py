import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class DJMaurice(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.music")
        await self.load_extension("cogs.fun")

        guild_id = os.getenv("GUILD_ID")
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            self.tree.copy_global_to(guild=guild)
            # Clear stale global commands, sync guild only
            await self.tree.sync(guild=guild)
            self.tree.clear_commands(guild=None)
            await self.tree.sync()
        else:
            await self.tree.sync()

        print(f"Synced {len(self.tree.get_commands())} slash commands.")

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} (ID: {self.user.id})")


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN not set. Copy .env.example to .env and add your token.")

    bot = DJMaurice()
    bot.run(token)


if __name__ == "__main__":
    main()
