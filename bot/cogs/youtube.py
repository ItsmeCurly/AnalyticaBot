import discord
import google
from discord.ext.commands import Cog, Bot, command, Context

class YouTube(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @command()
    def play(self, ctx, *, video_name: str) -> None:
        pass
    
def setup(bot) -> None:
    bot.add_cog(YouTube(bot))
    print("Loaded cog: YouTube")