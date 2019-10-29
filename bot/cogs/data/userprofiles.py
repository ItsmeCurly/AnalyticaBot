import sqlite3

import discord
from discord.ext.commands import Bot, Cog, Context, command

from bot.constants import database_path


class UserProfiles(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User) -> None:
        connect(after)

def connect(update: discord.User) -> None:
    conn = sqlite3.connect(database = database_path)
    c = conn.cursor()

    c.execute('INSERT INTO userprofiles (id, userid, name, guild_name, guild_display_name, avatar_url, created_at, last_updated, last_online) VALUES (?,?,?,?,?,?,?,?,?)')

    conn.close()

def setup(bot: Bot) -> None:
    bot.add_cog(UserProfiles(bot))
    print("Loaded cog: Data.UserProfiles")
