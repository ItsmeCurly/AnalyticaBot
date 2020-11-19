import discord
from discord.ext.commands import CheckFailure, Cog, Context, command

def try_get_value(_dict, key, default_val):
    return _dict[key] if key in _dict else default_val

async def find_message(ctx: Context, *args):
    if len(args) == 0:
        #do last message

        #possibly make this smarter so that it doesn't include any messages that are commands
        messages = await ctx.channel.history(limit=2).flatten()

        return messages[-1]
    elif len(args) == 1:
        #{typed_name, mention}
        member = find_member(ctx, username=args[0])
        if member == None:
            return await ctx.send("No member found for given argument")
        count = 2 if ctx.author == member else 1
        return find_message_helper(ctx, member, count=count)
        
    elif len(args) == 2:
        #{typed_name, mention} number
        #number signifies the number of messages back for that user, where 1 is the last message
        member = find_member(ctx, username=args[0])
        if member == None:
            return await ctx.send("No member found for given argument")
        count = args[1]+1 if ctx.author == member else args[1]
        return find_message_helper(ctx, member, count=count)

async def find_message_helper(ctx: Context, _member, _count):
    count = 0
    async for message in ctx.channel.history(limit=99999):
        if ctx.author == _member:
            count += 1
            if count == _count:
                return_message = message
                break
    return return_message

async def find_member(ctx: Context, username):
    if username is None:
        return ctx.author
    if len(ctx.message.mentions) > 0:
        member_list = []
        for mention in ctx.message.mentions:
            member_list.append(mention)
        return member_list[0] if len(member_list) == 1 else member_list
    else:
        members = ctx.guild.members
        member_names = []
        for member in members:
            if member.display_name is not member.name:
                member_names.append(member.nick)
            member_names.append(member.name)
        match = dl.get_close_matches(username, member_names, n=1)

        if len(match) > 0:
            member = discord.utils.find(
                lambda m: match in (m.name, m.nick), ctx.guild.members
            )
            return member
        else:
            return None