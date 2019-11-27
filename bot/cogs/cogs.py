import discord
from discord.ext.commands import Cog, Context, command

from bot.constants import MODERATION_ROLES
from bot.decorators import developer, with_roles


class Cogs(Cog):
    def __init__(self, bot):
        self.bot = bot

    @developer()
    @command()
    async def load(self, ctx: Context, *, extension_name: str) -> None:
        try:
            self.bot.load_extension('bot.cogs.' + extension_name)
        except:
            print(f"'{extension_name.title()}' already loaded")
        await ctx.send(f"{extension_name} loaded")

    @developer()
    @command()
    async def unload(self, ctx: Context, *, extension_name: str) -> None:
        print("test")
        try:
            self.bot.unload_extension('bot.cogs.' + extension_name)
        except:
            print("Extension not")
        await ctx.send(f"'{extension_name}' unloaded")

    @developer()
    @command()
    async def reload(self, ctx: Context, *, extension_name: str) -> None:
        try:
            self.bot.reload_extension('bot.cogs.' + extension_name)
        except:
            print(f"'{extension_name.title()}' not loaded")
        await ctx.send(f"{extension_name} reloaded")


def setup(bot):
    bot.add_cog(Cogs(bot))
    print("Loaded cog: Cogs")
