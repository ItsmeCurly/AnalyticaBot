import discord
from discord.ext import commands


class x(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(x(bot))
    print("Loaded x")
