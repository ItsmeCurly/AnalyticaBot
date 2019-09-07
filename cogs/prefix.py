import discord
from discord.ext import commands

import json

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, *pre):
        if len(pre) != 0 and len(pre) != 1:
            ctx.send("Prefix not changed, please supply a valid prefix")
            return
        pref = pre[0]

        with open(r"E:\Programs\AnalyticaBot\prefixes.json", 'r') as f:
            prefixes = json.load(f)
        guild_id = str(ctx.guild.id)

        if guild_id in prefixes.keys():
            guild_prefixes = prefixes[guild_id]
        else:
            guild_prefixes = {}

        author_id = str(ctx.author.id)

        guild_prefixes[author_id] = pref
        prefixes[guild_id] = guild_prefixes

        await ctx.send(f"New prefix is '{pref}'")

        with open(r"E:\Programs\AnalyticaBot\prefixes.json", 'w') as f:
            json.dump(prefixes, f, indent=4)

def setup(bot):
    bot.add_cog(Prefix(bot))
    print("Loaded prefix")
