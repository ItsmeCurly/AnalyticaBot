import discord
from discord.ext import commands

from bot.decorators import with_roles, developer
from bot.constants import MODERATION_ROLES

class Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def load_cog(self, ctx, *, extension_name: str):
        try:
            self.bot.load_extension('bot.cogs.' + extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send(f"{extension_name} loaded")

    @commands.is_owner()
    @commands.command()
    async def unload_cog(self, ctx, *, extension_name: str):
        self.bot.unload_extension('bot.cogs.' + extension_name)
        await ctx.send(f"{extension_name} unloaded")

    @commands.is_owner()
    @commands.command()
    async def reload_cog(self, ctx, *, extension_name: str):
        try:
            self.bot.unload_extension('bot.cogs.' + extension_name)
            self.bot.load_extension('bot.cogs.' + extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send(f"{extension_name} reloaded")

def setup(bot):
    bot.add_cog(Cogs(bot))
    print("Loaded cog: Cogs")
