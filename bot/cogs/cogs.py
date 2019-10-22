import discord

from bot.decorators import with_roles, developer
from bot.constants import MODERATION_ROLES

from discord.ext.commands import Context, command, Cog

class Cogs(Cog):
    def __init__(self, bot):
        self.bot = bot

    @developer()
    @command()
    async def load_cog(self, ctx: Context, *, extension_name: str) -> None:
        try:
            self.bot.load_extension('bot.cogs.' + extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send(f"{extension_name} loaded")

    @developer()
    @command()
    async def unload_cog(self, ctx: Context, *, extension_name: str) -> None:
        self.bot.unload_extension('bot.cogs.' + extension_name)
        await ctx.send(f"{extension_name} unloaded")

    @developer()
    @command()
    async def reload_cog(self, ctx: Context, *, extension_name: str) -> None:
        try:
            self.bot.reload_extension('bot.cogs.' + extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send(f"{extension_name} reloaded")

def setup(bot):
    bot.add_cog(Cogs(bot))
    print("Loaded cog: Cogs")
