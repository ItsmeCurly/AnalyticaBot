import pprint
import sqlite3
from datetime import datetime

import discord
from discord.ext.commands import Bot, Cog, Context, command

from bot.cogs.data.dbref import recent_message_connect
from bot.constants import DATABASE_PATH
from bot.decorators import developer
from bot.utils.database import print_table_structure
from bot.utils.helper_functions import try_get_value


class Messages(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, msg: discord.Message):
        if not msg.author.bot:
            await on_message_connect(msg)

    @Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        await on_message_edit_connect(after)

    @Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        await on_raw_message_edit_connect(payload)

    @command()
    async def message_get_last(self, ctx: Context, *, amt: int) -> None :
        await recent_message_connect(ctx = ctx, table_name='messages', amt=amt)

    @command()
    @developer()
    async def show_schema(self, ctx: Context):
        #await ctx.send()
        pass

async def on_message_connect(message: discord.Message) -> None:
    await connect(
        message_id=message.id,
        member_id=message.author.id,
        content=message.content,
        channel_id=message.channel.id,
        guild_id=message.guild.id if message.guild else -1,
        embeds=None,
        attachments=",".join(attachment.url for attachment in message.attachments),
        reactions=",".join(message.reactions.emoji),
        time=datetime.now(),
        edited=0,
        message_type="SEND_MESSAGE"
        )

async def on_message_edit_connect(message: discord.Message) -> None:
    await connect(
        message_id=message.id,
        member_id=message.author.id,
        content=message.content,
        channel_id=message.channel.id,
        guild_id=message.guild.id if message.guild else -1,
        embeds=None,
        attachments=",".join(attachment.url for attachment in message.attachments),
        reactions=",".join(message.reactions),
        time=datetime.now(),
        edited=1,
        message_type="EDIT_MESSAGE"
    )

async def on_raw_message_edit_connect(payload: discord.RawMessageUpdateEvent):
    if payload.cached_message:
        pass# return
    payload_dict = payload.data
    print(payload_dict)
    await connect(
        message_id=try_get_value(payload_dict, "id", None),
        member_id = payload_dict["author"]["id"] if "author" in payload_dict else -1,
        content=try_get_value(payload_dict, "content", None),
        channel_id=try_get_value(payload_dict, "channel_id", None),
        guild_id=try_get_value(payload_dict, "guild_id", None),
        embeds = None, #TODO
        # TODO
        attachments=(",".join(attachment['url'] for attachment in payload_dict['attachments']) if 'attachment' in payload_dict else None),
        reactions = None, #Cannot get reactions from message edit
        time = try_get_value(payload_dict, "edited_timestamp", None),
        edited = 1,
        message_type = "RAW_EDIT_MESSAGE"
    )

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
