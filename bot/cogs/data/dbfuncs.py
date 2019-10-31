import sqlite3
from datetime import datetime

import discord
from discord.ext.commands import Bot, Cog, Context, command

from bot.cogs.data.dbref import recent_message_connect
from bot.constants import database_path
from bot.decorators import developer
from bot.utils.database import create_messages_table, create_serverref_table, create_userprofiles_table


class DbFuncs(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    @developer
    def delete_table(self, ctx: Context, table_name:str) -> None:
        conn = sqlite3.connect(database_path)
        c = conn.cursor()

        c.execute(f"""DROP TABLE {table_name}""")

        conn.commit()
        conn.close()
    @command()
    @developer
    def create_table(self, ctx: Context, table_name: str) -> None:
        {
            'messages': create_messages_table,
            'serverref': create_serverref_table,
            'userprofiles': create_userprofiles_table
        }.get(table_name.lower(), lambda: None)()

def setup(bot) -> None:
    bot.add_cog(DbFuncs(bot))
    print("Loaded cog: Data.DbFuncs")
