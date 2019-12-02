import discord
from discord.ext.commands import Cog, command

class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f'Logged on as {self.bot.user}!')

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if not message.guild:
            print('Direct ', end = "")
        print(f'Message from {message.author}: {message.content}')

    @Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # channel = member.guild.system_channel
        # if channel is not None:
        #     await channel.send(f'Welcome {member.mention}!')
        pass

def setup(bot):
    bot.add_cog(Events(bot))
    print("Loaded cog: Events")
