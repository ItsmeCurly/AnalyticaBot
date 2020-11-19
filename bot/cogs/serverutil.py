import difflib as dl
import pprint
import time

import discord
from bot.constants import ACCEPTORS, MODERATION_ROLES, NEGATORS, SLURS
from bot.decorators import with_roles
from bot.utils.helper_functions import *
from discord.ext.commands import CheckFailure, Cog, Context, command
import re

class ServerUtil(Cog):
    def __init__(self, bot):
        self.bot = bot

    @with_roles(MODERATION_ROLES)
    @command()
    async def kick_user(self, ctx, *, name, reason):
        await self.bot.kick(name, reason=reason)

    @command()
    async def avatar(self, ctx: Context, *, member: discord.Member = None):
        """
        Returns the avatar of the person who called it if no parameters are
        sent, otherwise returns the avatar of the person mentioned
        """
        member = member or ctx.author
        await ctx.send(member.avatar_url)

    @command()
    async def avatars(self, ctx: Context, *members):
        """
        Returns the avatar of the person who called it if no parameters are
        sent, otherwise returns the avatar of the person mentioned
        """
        if members is None:
            await ctx.send("No users specified")
        elif ctx.message.mention_everyone:
            for i in ctx.guild.members:
                await ctx.send(i.avatar_url)
        else:
            for i in ctx.message.mentions:
                await ctx.send(i.avatar_url)

    @with_roles(MODERATION_ROLES)
    @command()
    async def kick_users(self, ctx, *names):

        for name in names:
            await self.bot.kick(name, reason=None)

    @with_roles(MODERATION_ROLES)
    @command()
    async def clear_messages(self, ctx: Context, user, amount, *channels):
        """Need to rewrite"""

        # messages = await ctx.channel.history(limit=amount).flatten()
        pass

    @with_roles(MODERATION_ROLES)
    @command()
    async def prune_members(self, ctx: Context, _days: int):
        """To fix and work on possibly"""

        estimate_prune = await ctx.guild.estimate_pruned_members(days=_days)
        await ctx.channel.send(f"Estimated prune members: {estimate_prune}")

    @command()
    @with_roles(MODERATION_ROLES)
    async def get_server_id(self, ctx):
        """
        Returns a server's id. Will return the id of the server from where it
        is requested.
        """

        await ctx.channel.send(f"This server's id is {ctx.guild.id}")

    @command()
    async def get_user_id(self, ctx):
        """Returns a user's id that requested it"""

        await ctx.channel.send(f"Your user id is {ctx.author.id}")

    @get_server_id.error
    async def get_server_id_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.send("You cannot call this function")

    # @with_roles(MODERATION_ROLES)
    # @command()
    # async def server_purge(self, ctx: Context, server_id1: int, server_id2: int):
    #     """
    #     Removes all the members from server_id1 that do not exist in
    #     server_id2. The bot must be present in both servers for this to
    #     function. Server ids can be gotten from !get_server_id within the
    #     server to get the id.
    #     """

    #     bot_server_list = self.bot.guilds

    #     server1, server2 = None, None

    #     for bot_server in bot_server_list:
    #         if bot_server.id == server_id1:
    #             server1 = bot_server
    #         if bot_server.id == server_id2:
    #             server2 = bot_server

    #     remove_list = []

    #     for member in server1.members:
    #         if member not in server2.members and not member.bot:
    #             remove_list.append(member)

    #     await ctx.send(f"This will remove {len(remove_list)} members")

    #     to_print = ""
    #     for member in remove_list:
    #         to_print += f"@{member.name}#{member.discriminator}, "
    #     if to_print:
    #         to_print = to_print[:-2]

    #     await ctx.send(f"Those members are: {to_print}")
    #     await ctx.send("Are you sure you would like to remove these members? (y/n)")

    #     done = False

    #     def check(msg: discord.Message):
    #         return msg.channel == ctx.message.channel

    #     while not done:
    #         msg = await self.bot.wait_for("message", check=check)

    #         if msg.content in ACCEPTORS:
    #             for member in remove_list:
    #                 await server1.kick(member)
    #                 await msg.channel.send(f"Kicked {member.mention}")
    #                 time.sleep(1)
    #             done = True

    #         elif msg.content in NEGATORS:
    #             await msg.channel.send(f'Server "{server1}" not purged')
    #             done = True

    #         elif msg.content.startswith("="):
    #             for member in remove_list:
    #                 await member.send(NATE_PURGE_MESSAGE)

    #         elif msg.content.startswith("-"):
    #             member = find_closest_user(remove_list, msg.content[1:])
    #             remove_list.remove(member)
    #             await msg.channel.send(
    #                 f"Member {member.name}#{member.discriminator} removed from list"
    #             )
    #             await msg.channel.send(f"Current list is {remove_list}")

    #         elif msg.content.startswith("+"):
    #             member = find_closest_user(server1.members, msg.content[1:])
    #             remove_list.append(member)
    #             await msg.channel.send(
    #                 f"Member {member.name}#{member.discriminator} added to list"
    #             )
    #             await msg.channel.send(
    #                 f"Current list is {remove_list if len(remove_list) > 0 else 'empty'}"
    #             )

    @command(name="nwordcount")
    async def nword_count(self, ctx: Context, *, username):
        """

        """
        member = await find_member(ctx, username)

        if member == None:
            return await ctx.send("No member found from arguments")
        else:
            word_1 = 0
            word_2 = 0
            async for channel in ctx.guild:
                async for message in channel.history(limit=100000):
                    if message.content.lower().contains(SLURS[0]):
                        word_1 += 1
                        word_2 += 1
                    if message.content.lower().contains(SLURS[1]):
                        word_1 += 1

            return await ctx.send(
                f"%s has said the nword %d times, of which %d were hard r's.",
                member.display_name,
                word_1,
                word_2,
            )


    @command(name="owoify")
    async def owoify(self, ctx: Context, *, args):
        """
        -u : Choose user
        -m : Add message
        """

        #case 1: message is contained within the command call

        """
        Cases:
            neither: no arguments, parse last message in chat
            user: starts with -u
            message: starts with -m
            message: encased by ""
            user: starts with mention in first position
            user: user in first position, probably need to check length of arguments for this
            message: raw string, parse this possibility last
        """

        split_args = args.split()

        first_word = split_args[0]

        if "@" in first_word and first_word[0] is not "\"":
            for mention in ctx.message.mentions:
                if mention.id in first_word
                    user = "@" + mention.display_name
        
        # message = await find_message(ctx, *args)

        # print(message.content)

        # print(ctx.channel.last_message.content)
        # await(ctx.send(message.content))

    @command(name="emojify")
    async def emojify(self, ctx: Context, *args):
        message = await find_message(ctx, *args)

        print(message.content)

def setup(bot):
    bot.add_cog(ServerUtil(bot))
    print("Loaded cog: ServerUtil")
