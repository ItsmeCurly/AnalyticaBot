import sqlite3
import pprint
from datetime import datetime

import discord
from discord.ext.commands import Bot, Cog, Context, command

from bot.constants import DATABASE_PATH
from bot.cogs.data.dbref import recent_message_connect


class UserProfiles(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        on_message_connect(message)

    @Cog.listener()
    async def on_user_update(self, before: discord.User,
                             after: discord.User) -> None:
        user_update_connect(after)

    @Cog.listener()
    async def on_member_update(self, before: discord.Member,
                               after: discord.Member) -> None:
        member_update_connect(after)

    @Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        member_join_connect(member)

    @Cog.listener()
    async def on_member_leave(self, member: discord.Member) -> None:
        member_leave_connect(member)

    @command()
    async def userprofiles_get_last(self, ctx: Context, amt: int) -> None:
        await recent_message_connect(ctx, 'userprofiles', amt)

    @command()
    async def full_update(self, ctx: Context) -> None:
        for member in ctx.message.guild.members:
            full_update_connect(member)

def on_message_connect(message: discord.Message) -> None:
    user=message.author
    connect(
        userid=user.id,
        discriminator=user.discriminator,
        name=user.name,
        avatar_url=str(user.avatar_url),
        activities=None,
        created_at=user.created_at,
        joined_at=None,
        update_type='SEND_MESSAGE'
    )

def user_update_connect(user: discord.User) -> None:
    connect(
        userid=user.id,
        discriminator=user.discriminator,
        name=user.name,
        avatar_url=str(user.avatar_url),
        activities=None,
        created_at=user.created_at,
        joined_at=None,
        update_type='UPDATE_USER'
    )

def full_update_connect(member: discord.Member) -> None:
    connect(
        userid=member.id,
        discriminator=member.discriminator,
        name=member.name,
        guild_id=member.guild.id,
        guild_user_display_name=member.display_name,
        avatar_url=str(member.avatar_url),
        premium_since=member.premium_since,
        status=get_status(member.status),
        mobile_status=get_status(member.mobile_status),
        desktop_status=get_status(member.desktop_status),
        web_status=get_status(member.web_status),
        roles=','.join(role.name for role in member.roles),
        activities=','.join(activity.name for activity in member.activities),
        created_at=member.created_at,
        joined_at=member.joined_at,
        update_type='UDPATE_FULL_MEMBER'
    )

def member_update_connect(member: discord.Member) -> None:
    connect(
        userid=member.id,
        discriminator=member.discriminator,
        name=member.name,
        guild_id=member.guild.id,
        guild_user_display_name=member.display_name,
        avatar_url=str(member.avatar_url),
        premium_since=member.premium_since,
        status=get_status(member.status),
        mobile_status=get_status(member.mobile_status),
        desktop_status=get_status(member.desktop_status),
        web_status=get_status(member.web_status),
        roles=','.join(role.name for role in member.roles),
        activities=','.join(activity.name for activity in member.activities),
        created_at=member.created_at,
        joined_at=member.joined_at,
        update_type='UPDATE_MEMBER'
    )

def member_join_connect(member: discord.Member) -> None:
    connect(
        userid=member.id,
        discriminator=member.discriminator,
        name=member.name,
        guild_id=member.guild.id,
        guild_user_display_name=member.display_name,
        avatar_url=str(member.avatar_url),
        premium_since=member.premium_since,
        status=get_status(member.status),
        mobile_status=get_status(member.mobile_status),
        desktop_status=get_status(member.desktop_status),
        web_status=get_status(member.web_status),
        roles=','.join(role.name for role in member.roles),
        activities=','.join(activity.name for activity in member.activities),
        created_at=member.created_at,
        joined_at=member.joined_at,
        update_type='JOIN_MEMBER'
    )

def member_leave_connect(member: discord.Member) -> None:
    connect(
        userid=member.id,
        discriminator=member.discriminator,
        name=member.name,
        guild_id=member.guild.id,
        guild_user_display_name=member.display_name,
        avatar_url=str(member.avatar_url),
        premium_since=member.premium_since,
        status=get_status(member.status),
        mobile_status=get_status(member.mobile_status),
        desktop_status=get_status(member.desktop_status),
        web_status=get_status(member.web_status),
        roles=','.join(role.name for role in member.roles),
        activities=','.join(activity.name for activity in member.activities),
        created_at=member.created_at,
        joined_at=member.joined_at,
        update_type='LEAVE_MEMBER'
    )

def connect(*, userid:int, discriminator:int = -1, name:str, guild_id:int = -1,
            guild_user_display_name:str = "", avatar_url:str,
            premium_since:datetime = None, status=None, mobile_status=None,
            desktop_status=None, web_status=None, roles=None, activities,
            created_at, joined_at, last_updated=datetime.utcnow(), last_online=
            datetime.utcnow(), update_type: str) -> None:
    """Helper function to connect to database, passed with many parameters to
    supplement a large query"""

    with sqlite3.connect(database=DATABASE_PATH) as conn:
        c = conn.cursor()

        c.execute("""INSERT INTO userprofiles(
                userid,
                discriminator,
                name,
                guild_id,
                guild_user_display_name,
                avatar_url,
                premium_since,
                status,
                mobile_status,
                desktop_status,
                web_status,
                roles,
                activities,
                created_at,
                joined_at,
                last_updated,
                last_online,
                update_type
                )
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                [
                    userid,
                    discriminator,
                    name,
                    guild_id,
                    guild_user_display_name,
                    avatar_url,
                    premium_since,
                    status,
                    mobile_status,
                    desktop_status,
                    web_status,
                    roles,
                    activities,
                    created_at,
                    joined_at,
                    last_updated,
                    last_online,
                    update_type
                ])
        conn.commit()

def get_status(status: discord.Status):
    if status == discord.Status.online:
        return 'Online'
    elif status == discord.Status.idle:
        return 'Idle'
    elif status == discord.Status.dnd:
        return 'DnD'
    elif status == discord.Status.offline:
        return 'Offline'
    return 'None'

def compare_changes(before: discord.Member, after: discord.Member) -> str:
    """Function will take changes between two member objects and attempt to find
    the difference between them"""
    _str = ""
    if before.id != after.id:
        _str += 'id'
    if before.discriminator != after.discriminator:
        _str += 'discriminator'
    if before.name != after.name:
        _str += 'name'
    if before.guild.id != after.guild.id:
        _str += 'guild.id'
    if before.display_name != after.display_name:
        _str += 'display_name'
    if before.avatar_url != after.avatar_url:
        _str += 'avatar_url'
    if before.premium_since != after.premium_since:
        _str += 'premium_since'
    if before.status != after.status:
        _str += 'status'
    if before.mobile_status != after.mobile_status:
        _str += 'mobile_status'
    if before.desktop_status != after.desktop_status:
        _str += 'desktop_status'
    if before.web_status != after.web_status:
        _str += 'web_status'
    if before.roles != after.roles:
        _str += 'roles'
    if before.activities != after.activities:
        _str += 'activities'
    return _str

def setup(bot: Bot) -> None:
    bot.add_cog(UserProfiles(bot))
    print("Loaded cog: Data.UserProfiles")
