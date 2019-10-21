import discord

from discord.ext import commands

def is_admin(member):
    return member.guild_permissions == discord.Permissions.administrator
def is_owner(member):
    return member.id == discord.Guild.owner
        
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
    async def clear_messages(self, ctx, user, amount, *channels):
        #messages = await ctx.channel.history(limit=amount).flatten()
        pass
    
    @commands.command()
    async def prune_members(self, ctx, _days: int):
        if not is_admin(ctx.author) and is_owner(ctx.author):
            await ctx.channel.send(f"Only admins can call this role: {ctx.author.guild_permissions}")
            return
        estimate_prune = await ctx.guild.estimate_pruned_members(days = _days)
        await ctx.channel.send(f"Estimated prune members: {estimate_prune}")
        

def setup(bot):
    bot.add_cog(ServerUtil(bot))
    print("Loaded serverutil")
