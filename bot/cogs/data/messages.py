import discord

from discord.ext.commands import Bot, command, Cog

class Messages(Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(Messages(bot))
    print("Loaded cog: Data.Messages")
