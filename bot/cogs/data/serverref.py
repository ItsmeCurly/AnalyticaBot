import sqlite3

import discord
from discord.ext.commands import Bot, Cog, command

from bot.constants import DATABASE_PATH

class ServerRef(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel,
                                      after: discord.abc.GuildChannel):
        connect(after)

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        pass

async def connect(message: discord.Message):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute(sql="""INSERT INTO serverref (guild_id, guild_name, channel,
              channel_name, last_channel_update, last_channel_activity,
              last_guild_update, last_guild_activity)
              VALUES(?,?,?,?,?,?,?,?,?)""",
    )

    conn.close()

def setup(bot):
    bot.add_cog(ServerRef(bot))
    print("Loaded cog: Data.ServerRef")
