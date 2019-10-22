import discord
import urllib
from discord.ext import commands

class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create_emoji(self, ctx, arg1, arg2):
        #ctx.send("Create_emoji")
        name = arg1

        #urllib.request.urlretrieve

def setup(bot):
    bot.add_cog(Emoji(bot))
    print("Loaded cog: Emoji")
