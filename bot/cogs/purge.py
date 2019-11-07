import discord
from discord.utils import get

from discord.ext.commands import command, Context
from bot.decorators import with_roles
from bot.constants import MODERATION_ROLES
from datetime import datetime, date

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command()
    @with_roles(MODERATION_ROLES)
    def delete_user_messages(self, ctx: Context, user: str, *after: str):
        pass

def setup(bot):
    bot.add_cog(Purge(bot))
    print("Loaded cog: Purge")
