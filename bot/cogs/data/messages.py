import sqlite3
from datetime import datetime
import pprint
import discord
from discord.ext.commands import Bot, Cog, Context, command

from bot.cogs.data.dbref import recent_message_connect
from bot.constants import DATABASE_PATH
from bot.decorators import developer
from bot.utils.database import print_table_structure


class Messages(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @Cog.listener()
    async def on_message(self, msg: discord.Message):
        if not msg.author.bot:
            await on_message_connect(msg)
            
    @Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        await on_raw_message_edit_connect(payload)
        
    @command()
    async def message_get_last(self, ctx: Context, *, amt: int) -> None :
        await recent_message_connect(table_name='messages', amt=amt)
        
    @command()
    @developer()
    async def show_schema(self, ctx: Context):
        await ctx.send()

async def on_message_connect(message: discord.Message) -> None:
    await connect(
        message.id,  
        message.author.id,
        message.content,
        message.channel.id,
        message.guild.id if message.guild else -1,
        ",".join(message.embeds),
        ",".join(message.attachments),
        ",".join(message.reactions),
        datetime.now(),
        0,
        "SEND_MESSAGE"
        )
    
async def on_raw_message_edit_connect(payload: discord.RawMessageUpdateEvent):
    if payload.cached_message:
        pass# return
    payload_dict = payload.data
    print(payload_dict)

async def connect(message_id: int, member_id: int, content: str, 
                  channel_id: int, guild_id: int, embeds: str, attachments: str,
                  reactions: str, time: datetime, edited: int, 
                  message_type: str):
    
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()

        c.execute("""INSERT INTO messages (
            message_id,
            member_id, 
            content, 
            channel_id, 
            guild_id,
            embeds,
            attachments,
            reactions,
            time,
            edited,
            message_type
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)""", 
            [
                message_id,
                member_id,
                content,
                channel_id,
                guild_id,
                embeds,
                attachments,
                reactions,
                time,
                edited,
                message_type
            ])

        conn.commit()

def setup(bot):
    bot.add_cog(Messages(bot))
    print("Loaded cog: Data.Messages")
