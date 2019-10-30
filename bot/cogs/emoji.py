import urllib

import discord
from discord.ext import commands

from bot.constants import MODERATION_ROLES
from bot.decorators import with_roles


class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @with_roles(MODERATION_ROLES, 'manage_emojis')
    @commands.command()
    async def create_emoji(self, ctx, arg1, arg2):
        #ctx.send("Create_emoji")
        name = arg1

        #urllib.request.urlretrieve

def setup(bot):
    bot.add_cog(Emoji(bot))
    print("Loaded cog: Emoji")
