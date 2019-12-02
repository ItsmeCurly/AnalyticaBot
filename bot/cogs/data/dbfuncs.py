import sqlite3
from datetime import datetime

import discord
from discord.ext.commands import Bot, Cog, Context, command

from bot.constants import ACCEPTORS, NEGATORS, DATABASE_PATH
from bot.decorators import developer
from bot.utils.database import (create_messages_table, create_serverref_table,
                                create_userprofiles_table, pprint_table_structure)


class DbFuncs(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    @developer()
    async def delete_table(self, ctx: Context, table_name:str) -> None:
        self.waiting_delete_table = True
        self.table_name = table_name
        await ctx.send(f"Would you like to delete {table_name}? (Y/N)")

        def check(msg: discord.Message):
            return ctx.message.channel == msg.channel

        msg = await self.bot.wait_for('message', check=check)

        if msg.content.lower() in ACCEPTORS:
            delete_table_func(self.table_name)
            await msg.channel.send(f"Successfully deleted {table_name}")

        elif msg.content.lower() in NEGATORS:
            await msg.channel.send(f"{table_name} not deleted")

    @command()
    @developer()
    async def create_table(self, ctx: Context, table_name: str) -> None:
        {
            'messages': create_messages_table,
            'serverref': create_serverref_table,
            'userprofiles': create_userprofiles_table
        }.get(table_name.lower(), lambda: None)()

def delete_table_func(table_name):
    """Function to delete the table after the user has accepted the prompt"""

    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute(f"""DROP TABLE {table_name}""")

    conn.commit()
    conn.close()

def setup(bot) -> None:
    bot.add_cog(DbFuncs(bot))
    print("Loaded cog: Data.DbFuncs")
