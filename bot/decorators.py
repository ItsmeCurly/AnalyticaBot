import discord

from discord.ext import commands
from bot.utils.checks import with_role_check, developer_check

def with_roles(role_ids: tuple) -> callable:
    async def predicate(ctx):
        return with_role_check(ctx, role_ids)
    return commands.check(predicate)

def developer() -> callable:
    async def predicate(ctx):
        return developer_check(ctx)
    return commands.check(predicate)
