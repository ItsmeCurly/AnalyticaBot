import discord
from discord import opus
import youtube_dl

from bot.utils.video_downloader import Downloader

from discord.ext.commands import command, Context, Bot, Cog

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

class Music(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.downloader = Downloader()
        load_opus_lib()

    @command()
    async def join(self, ctx: Context):
        if not (chan := ctx.author.voice.channel):
            return
        self.voice_client = await chan.connect()

    @command(aliases=['lv'])
    async def leave(self, ctx:Context):
        if not self.voice_client:
            return
        await self.voice_client.disconnect()
        self.voice_client = None

    @command(aliases=['paly'])
    async def play(self, ctx: Context, sound_name: str):
        """Need to handle when user inputs song from spotify, playlist from
        spotify, song from youtube, playlist from youtube, song from soundcloud,

        """
        audio = create_audio_source(sound_name)
        self.voice_client.play(audio, after=None)

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
    audio = discord.FFmpegPCMAudio(source="music\\video.mp3")
    return audio

def setup(bot):
    bot.add_cog(Music(bot))
    print("Loaded cog: Music")
