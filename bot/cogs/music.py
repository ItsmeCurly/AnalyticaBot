from multiprocessing import Process
import sys
import importlib

import discord
import spotipy
import youtube_dl
from discord import opus
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio
import functools
import aiohttp
import html5lib


from bot.exceptions import AnalyticaError

from bot.utils.video_downloader import Downloader

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll',
             'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

class SoundSource(discord.PCMVolumeTransformer):

    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, data: dict, volume: float = 0.5):
        super().__init__(source, volume)
        self.volume = volume

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop if loop else asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)

        data = await loop.run_in_executor(None, partial)

        if data is None:
            print('Nothing found at URL')
            return

        webpage_url = data['webpage_url']

        partial = functools.partial(cls.ytdl.extract_info, webpage_url,
                                    download=False)
        processed_data = await loop.run_in_executor(None, partial)

        if processed_data is None:
            print('No processed data found at URL')
            return

        info = processed_data

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)


class Song:
    def __init__(self, source: SoundSource):
        self.source = source


class SongQueue(asyncio.Queue):

    async def clear(self):
        while not self.empty():
            self.get()

class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context, *, voice_client = None):
        self.bot = bot
        self.ctx = ctx

        self.current_song = None
        self.voice_client = None
        self.next_song = asyncio.Event()
        self.songs = SongQueue()

        self._volume = 0.5

        self.audio_player = bot.loop.create_task(self.play_audio_player())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def volume(self):
        return self._volume

    @property
    def is_playing(self):
        return self.voice_client and self.current_song

    async def play_audio_player(self):
        """Audio player coroutine. Will play infinitely"""
        #TODO: Performance measures
        while True:
            #set asyncio flag to false for now
            self.next_song.clear()

            #get next song from queue
            self.current_song = await self.songs.get()

            self.current_song.source.volume = self.volume
            #play next song, queue up next song with play_next_song
            self.voice_client.play(source=self.current_song.source, after=self.play_next_song)

            await self.next_song.wait()

    def play_next_song(self):
        """Sets the flag to true to allow for the wait() request to exit"""
        self.next_song.set()

    async def stop(self):
        """Clears the voice_state and disconnects the voice_client"""
        self.songs.clear()

        await self.voice_client.disconnect()
        self.voice_client = None


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sp = spotipy_setup_client_credentials()

        self.voice_states = {}

        load_opus_lib()

    async def get_voice_state(self, ctx: commands.Context):
        voice_state = self.voice_states.get(ctx.guild.id)

        if not voice_state:
            voice_state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = voice_state
        return voice_state

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = await self.get_voice_state(ctx)


    @commands.command()
    async def join(self, ctx: commands.Context):
        if not (author_voice := ctx.author.voice):
            return await ctx.send("You are not in a voice channel for me to join")
        if ctx.voice_state.voice_client:
            return await ctx.send("I am already in a voice channel, use summon to move me from my current voice channel")
        voice = await author_voice.channel.connect()

        ctx.voice_state.voice_client = voice

    @commands.command(aliases=['lv'])
    async def leave(self, ctx: commands.Context):
        if not ctx.voice_state.voice_client:
            return await ctx.send("I am not presently in a voice channel")
        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(aliases=['paly'])
    async def play(self, ctx: commands.Context, sound_name: str):
        # if "http://" in sound_name or "https://" in sound_name:
        #     if "open.spotify.com" in sound_name:
        #         if "playlist" in sound_name:
        #             #get the playlist, must use 'spotify' for login
        #             playlist = self.sp.user_playlist('spotify',
        #                                             playlist_id=sound_name)
        #             #get a list of the tracks in the playlist
        #             playlist_tracks = playlist['tracks']

        #             #have to reference each item specifically
        #             playlist_items = playlist_tracks['items']
        #             for item in playlist_items:
        #                 #get the track information
        #                 track = item['track']

        #                 #get the artists information
        #                 artists = track['artists']

        #                 #group all the artists names together into a string for
        #                 #searching on YouTube
        #                 artists_name = ""
        #                 for artist in artists:
        #                     artists_name += artist['name'] + " "

        #                 song = await self.create_song_from_source(ctx, artists_name.strip() + track['name'])

        #                 await ctx.voice_state.songs.put(song)
        # else:
        song = await self.create_song_from_source(ctx, sound_name)

        await ctx.voice_state.songs.put(song)

    async def create_song_from_source(self, ctx, sound_name):
        source = await SoundSource.create_source(ctx, sound_name, loop=self.bot.loop)

        return Song(source)

def load_opus_lib():
    if opus.is_loaded():
        return True

    for opus_lib in OPUS_LIBS:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass
        raise RuntimeError('Could not load an opus lib. Tried %s' %
                           (', '.join(OPUS_LIBS)))

def spotipy_setup_client_credentials():
    client_credentials_manager = SpotifyClientCredentials(
        client_id='d6868e900537402197e3ced73f10a6cf', client_secret='e69173223a6441da9b0ab80c2bc6c777')
    return spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)

def get_response(search: str):
    pass


def setup(bot):
    bot.add_cog(Music(bot))
    print("Loaded cog: Music")
