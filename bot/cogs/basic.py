import discord
from discord.ext import commands

from bot.decorators import with_roles, developer
from bot.constants import MODERATION_ROLES

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @developer()
    @commands.command()
    async def test(self, ctx: commands.Context):
        print("Test2")
        await ctx.send(ctx.author.status)


def setup(bot):
    bot.add_cog(Basic(bot))
    print("Loaded cog: Basic")
