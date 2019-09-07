import discord
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load(self, ctx, extension_name: str):
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            print("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        print("{} loaded.".format(extension_name))

    @commands.command()
    async def unload(self, ctx, extension_name: str):
        self.bot.unload_extension(extension_name)
        print("{} unloaded.".format(extension_name))

    @commands.command()
    async def reload(self, ctx, extension_name: str):
        try:
            self.bot.reload_extension(extension_name)
        except (AttributeError, ImportError) as e:
            print("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        print("{} loaded.".format(extension_name))

def setup(bot):
    bot.add_cog(Basic(bot))
    print("Loaded basic")
