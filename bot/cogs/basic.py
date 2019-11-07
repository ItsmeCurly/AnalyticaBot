import discord
from discord.ext.commands import command, Context, Cog

from bot.decorators import with_roles, developer
from bot.constants import MODERATION_ROLES

class Basic(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @developer()
    @command()
    async def shutdown(self, ctx: Context):
        self.bot.close()

    @developer()
    @command()
    async def test(self, ctx: Context) -> None:
        print("Test2")
        await ctx.send(ctx.author.status)


def setup(bot):
    bot.add_cog(Basic(bot))
    print("Loaded cog: Basic")
