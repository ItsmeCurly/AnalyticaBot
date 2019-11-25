import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged on as {self.bot.user}!')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if not message.guild:
            print('Direct ', end = "")
        print(f'Message from {message.author}: {message.content}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # channel = member.guild.system_channel
        # if channel is not None:
        #     await channel.send(f'Welcome {member.mention}!')
        pass

def setup(bot):
    bot.add_cog(Events(bot))
    print("Loaded cog: Events")
