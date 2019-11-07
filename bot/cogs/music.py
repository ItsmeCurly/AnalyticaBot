import discord
from discord import opus
import youtube_dl

from discord.ext.commands import command, Context, Bot, Cog

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

class Music(Cog):
    def __init__(self, bot):
        self.bot = bot
        load_opus_lib()

    @command()
    async def play(self, ctx: Context, sound_name: str):
        pass
      
def load_opus_lib():
    if opus.is_loaded():
        return True

    for opus_lib in OPUS_LIBS:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass
        raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(OPUS_LIBS)))  
        
def create_audio_source(file_name: str) -> discord.AudioSource:
    discord.FFmpegPCMAudio()

def setup(bot):
    bot.add_cog(Music(bot))
    print("Loaded cog: Music")