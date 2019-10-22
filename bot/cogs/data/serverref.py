import discord
import sqlite3

from bot.constants import database_path

from discord.ext.commands import Bot, command, Cog

class ServerRef(Cog):
    def __init__(self, bot):
        self.bot = bot
        
async def connect(message: discord.Message):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    
    c.execute(sql="INSERT INTO serverref (id, guild_id, guild_name, channel, channel_name, last_channel_update, last_channel_activity, last_guild_update, last_guild_activity) VALUES (?,?,?,?,?,?,?,?,?)")

def setup(bot):
    bot.add_cog(ServerRef(bot))
    print("Loaded cog: Data.ServerRef")
