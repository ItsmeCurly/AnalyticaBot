import discord
import sqlite3

from bot.constants import database_path

from discord.ext.commands import Bot, command, Cog, Context


class UserProfiles(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User) -> None:
        pass

def connect(update: discord.User) -> None:
    conn = sqlite3.connect(database = database_path)
    c = conn.cursor()

    c.execute('INSERT INTO userprofiles (id, userid, name, guild_name, guild_display_name, avatar_url, created_at, last_updated, last_online) VALUES (?,?,?,?,?,?,?,?,?)')

    conn.close()

def setup(bot):
    bot.add_cog(UserProfiles(bot))
    print("Loaded cog: Data.UserProfiles")



