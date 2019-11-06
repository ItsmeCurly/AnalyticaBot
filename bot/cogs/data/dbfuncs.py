import sqlite3
from datetime import datetime

import discord
from discord.ext.commands import Bot, Cog, Context, command

from bot.constants import ACCEPTORS, DENIERS, DATABASE_PATH
from bot.decorators import developer
from bot.utils.database import (create_messages_table, create_serverref_table,
                                create_userprofiles_table, pprint_table_structure)


class DbFuncs(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.waiting_delete_table = False
        self.table_name = ""
        
    @Cog.listener()    
    async def on_message(self, message: discord.Message):
        if message.content.lower() in ACCEPTORS:
            if self.waiting_delete_table:
                delete_table_func(self.table_name)
                self.waiting_delete_table = False
                self.table_name = ""
                await message.channel.send(f"Successfully deleted table {table_name}")
                
        elif message.content.lower() in DENIERS:
            if self.waiting_delete_table:
                self.waiting_delete_table = False
                self.table_name = ""
        
    @command()
    @developer()
    async def delete_table(self, ctx: Context, table_name:str) -> None:
        self.waiting_delete_table = True
        self.table_name = table_name
        await ctx.send(f"Would you like to delete {table_name}? (Y/N)")
    
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
