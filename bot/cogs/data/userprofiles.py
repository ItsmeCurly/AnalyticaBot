import discord
import sqlite3

from bot.constants import database_path
from datetime import datetime

from discord.ext.commands import Bot, command, Cog, Context


class UserProfiles(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User) -> None:
        pass

    @Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        member_connect(after)

def user_connect(user: discord.User) -> None:
    conn = sqlite3.connect(database = database_path)
    c = conn.cursor()

    c.execute('INSERT INTO userprofiles (userid, name, guild_name, guild_display_name, avatar_url, created_at, last_updated, last_online) VALUES (?,?,?,?,?,?,?,?,?)',
              (user.id, user.name, "", user.display_name, user.avatar_url, user.created_at, ))

    conn.close()

def member_connect(member: discord.Member) -> None:
    conn = sqlite3.connect(database=database_path)
    c = conn.cursor()

    c.execute('INSERT INTO userprofiles (userid, name, guild_name, guild_display_name, avatar_url, created_at, last_updated, last_online) VALUES (?,?,?,?,?,?,?,?,?)',
    ())

    conn.close()

def setup(bot):
    bot.add_cog(UserProfiles(bot))
    print("Loaded cog: Data.UserProfiles")
