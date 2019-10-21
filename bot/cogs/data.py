import discord
import sqlite3
from datetime import datetime
from discord.ext import commands

class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await connect(message)

    @commands.command()
    async def get_recent_messages(self, ctx, amount):
        await recent_message_connect(ctx, amount)

async def connect(message):
    if not message.author.bot:
        conn = sqlite3.connect("db\\analyticaDataPoints.db")
        c = conn.cursor()

        c.execute('INSERT INTO messages (member, content, channel, guild, time) VALUES (?,?,?,?,?)',
                (message.author.id, message.content, message.channel.id, message.guild.id, datetime.now()))

        conn.commit()
        conn.close()

async def recent_message_connect(ctx, amt):
    conn = sqlite3.connect("db\\analyticaDataPoints.db")
    c = conn.cursor()

    for row_message in c.execute('SELECT * FROM messages ORDER BY id DESC LIMIT ' + amt):
        await ctx.send(row_message)

    conn.close()

def setup(bot):
    bot.add_cog(Data(bot))
    print("Loaded data")
