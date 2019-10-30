import sqlite3
from datetime import datetime

import discord
from discord.ext.commands import Bot, Cog, Context, command

from bot.cogs.data.dbref import recent_message_connect
from bot.constants import database_path
from bot.decorators import developer
from bot.utils.database import print_table_structure


class DbFuncs(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @command()
    @developer
    def delete_table(self, ctx: Context, table_name:str) -> None:
        pass
        
def setup(bot) -> None:
    bot.add_cog(DbFuncs(bot))
    print("Loaded cog: Data.DbFuncs")
