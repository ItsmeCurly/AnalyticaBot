import discord

from discord.ext.commands import Bot, command, Cog


class ServerRef(Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(ServerRef(bot))
    print("Loaded cog: Data.ServerRef")
