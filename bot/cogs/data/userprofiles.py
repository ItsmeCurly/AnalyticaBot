import discord

from discord.ext.commands import Bot, command, Cog


class UserProfiles(Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(UserProfiles(bot))
    print("Loaded cog: Data.UserProfiles")
