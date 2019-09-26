import discord

from discord.ext import commands

class ServerUtil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def kick_user(self, ctx, *, name, reason):
        await self.bot.kick(name, reason = reason)
    
    @commands.command()
    async def kick_users(self, ctx, *names):
        for name in names:
            await self.bot.kick(name, reason = None)
    
    #TODO
    @commands.command()
    async def clear_messages(self, ctx, user, amount, *, channels):
        messages = await ctx.channel.history(limit=amount).flatten()
        
def setup(bot):
    bot.add_cog(ServerUtil(bot))
    print("Loaded serverutil")
