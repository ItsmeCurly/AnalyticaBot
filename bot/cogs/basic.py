import discord
from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load_cog(self, ctx, *, extension_name: str):
        try:
            self.bot.load_extension('cogs.' + extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} loaded".format(extension_name))

    @commands.command()
    async def unload_cog(self, ctx, *, extension_name: str):
        self.bot.unload_extension('cogs.' + extension_name)
        await ctx.send("{} unloaded".format(extension_name))

    @commands.command()
    async def reload_cog(self, ctx, *, extension_name: str):
        try:
            self.bot.unload_extension('cogs.' + extension_name)
            self.bot.load_extension('cogs.' + extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} reloaded".format(extension_name))

    @commands.command()
    async def test(self, ctx):
        print("Test2")
        await ctx.send("Test2")


def setup(bot):
    bot.add_cog(Basic(bot))
    print("Loaded basic")
