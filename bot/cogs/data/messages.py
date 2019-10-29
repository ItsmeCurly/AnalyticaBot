import sqlite3
from datetime import datetime

import discord
from discord.ext.commands import Bot, Cog, Context, command

from bot.cogs.data.dbref import recent_message_connect
from bot.constants import database_path
from bot.decorators import developer
from bot.utils.database import print_table_structure


class Messages(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @Cog.listener()
    async def on_message(self, msg: discord.Message):
        await connect(msg)
        
    @command()
    async def message_get_last(self, ctx: Context, *, amt: int) -> None :
        await recent_message_connect(table_name='messages', amt=amt)
        
    @command()
    @developer()
    async def show_schema(self, ctx: Context):
        await ctx.send()
    
async def connect(message: discord.Message):
    if not message.author.bot:
        conn = sqlite3.connect(database_path)
        c = conn.cursor()

        c.execute("""INSERT INTO messages (member, content, channel, guild, 
                  time) VALUES (?,?,?,?,?)""", 
                  [message.author.id, message.content, message.channel.id, 
                   message.guild.id, datetime.now()])

        conn.commit()
        conn.close()

def setup(bot):
    bot.add_cog(Messages(bot))
    print("Loaded cog: Data.Messages")
