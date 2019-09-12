import discord
import sqlite3

from datetime import datetime
from discord.ext import commands


class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        connect(message, "E:\\Programs\\db", "analyticaDataPoints.db")

    @commands.command()
    async def get_recent_messages(self, ctx, amount):
        pass

def connect(message, db_loc, db_filename):
    if not message.author.bot:
        conn = sqlite3.connect(db_loc + "\\" + db_filename)
        c = conn.cursor()

        c.execute('INSERT INTO messages (member, content, channel, guild, time) VALUES (?,?,?,?,?)',
                (message.author.id, message.content, message.channel.id, message.guild.id, datetime.now()))

        conn.commit()
        conn.close()

def setup(bot):
    bot.add_cog(Data(bot))
    print("Loaded data")
