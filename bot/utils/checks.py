import discord

from discord.ext import commands


def with_role_check(ctx: commands.Context, role_ids: tuple) -> bool:
    if not ctx.message.guild:
        return

    list_roles = list(iter(ctx.author.guild_permissions))

    for role_tuple in list_roles:
        if role_tuple[1] and role_tuple[0] in role_ids:
            return True
    return False

def is_guild_owner(ctx: commands.Context):
    return ctx.author == ctx.guild.owner_id

def developer_check(ctx: commands.Context) -> bool:
    print (ctx.bot.owner_id)
    return (ctx.author.id == 193943254545334272 or
            ctx.author.id == 625754791624310785)
