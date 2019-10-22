import discord
from discord.ext import commands
from bot.decorators import with_roles
from bot.constants import MODERATION_ROLES, prefixes_path

import json

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_prefix(self, ctx, *pre):
        if len(pre) == 0:
            await ctx.send("Prefix not changed, please supply a valid prefix")

        pref = pre[0]

        with open(prefixes_path, 'r') as f:
            prefixes = json.load(f)
        guild_id = str(ctx.guild.id)

        if guild_id in prefixes.keys():
            guild_prefixes = prefixes[guild_id]
        else:
            guild_prefixes = {}

        guild_prefixes[str(ctx.author.id)] = pref
        prefixes[guild_id] = guild_prefixes

        await ctx.send(f"New prefix is '{pref}'")

        with open(prefixes_path, 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.command()
    async def get_prefix(self, ctx):
        if not ctx.message.guild:
            pass

        with open(prefixes_path, 'r') as file:
            prefixes = json.load(file)
        guild_id = str(ctx.message.guild.id)

        if guild_id not in prefixes:
            await ctx.send('Your only prefix is \'!\'')

        author_id = str(ctx.message.author.id)
        if author_id not in prefixes[guild_id] or prefixes[guild_id][author_id] == '!':
            await ctx.send('Your only prefix is \'!\'')
            return

        all_prefix = (prefixes[guild_id][author_id], '!')

        await ctx.send(f"Your prefixes are {', '.join(all_prefix)}")

    @with_roles(*MODERATION_ROLES)
    @commands.command()
    async def set_server_prefix(self, ctx, *pre):
        if len(pre) == 0:
            await ctx.send("Prefix not changed, please supply a valid prefix")
            return

        pref = pre[0]

        with open(prefixes_path, 'r') as f:
            prefixes = json.load(f)
        guild_id = str(ctx.guild.id)

        if guild_id in prefixes.keys():
            guild_prefixes = prefixes[guild_id]
        else:
            guild_prefixes = {}

        for user in ctx.message.guild.members:
            if not user.bot:
                guild_prefixes[str(user.id)] = pref

        prefixes[guild_id] = guild_prefixes
        await ctx.send(f"New prefix for the server is '{pref}'")

        with open(prefixes_path, 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.command()
    async def reset_prefix(self, ctx):
        with open(prefixes_path, 'r') as f:
            prefixes = json.load(f)
        guild_id = str(ctx.guild.id)

        if guild_id in prefixes.keys():
            guild_prefixes = prefixes[guild_id]
        else:
            guild_prefixes = {}

        guild_prefixes[str(ctx.message.author.id)] = '!'
        prefixes[guild_id] = guild_prefixes

        await ctx.send("Prefix reset back to \'!\'")

        with open(prefixes_path, 'w') as f:
            json.dump(prefixes, f, indent=4)

def setup(bot):
    bot.add_cog(Prefix(bot))
    print("Loaded cog: Prefix")