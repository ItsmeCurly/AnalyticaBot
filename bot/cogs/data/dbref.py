import discord
import sqlite3
from bot.constants import database_path

from discord.ext.commands import Context

async def recent_message_connect(ctx: Context, table_name: str, amt: int) -> None:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    for row_message in c.execute(f'SELECT * FROM {table_name} ORDER BY id DESC LIMIT ' + amt):
        await ctx.send(row_message)

    conn.close()