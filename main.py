import discord
import json
import configparser
import six
import bot.utils.startup as startup


from bot.utils.prefix import get_prefix
from discord.ext import commands

bot = commands.Bot(command_prefix=get_prefix,
                   case_insensitive = True,
                   activity = discord.Game("halp me"))

bot.load_extension('bot.cogs.prefix')
bot.load_extension('bot.cogs.basic')
bot.load_extension('bot.cogs.events')
bot.load_extension('bot.cogs.emoji')
bot.load_extension('bot.cogs.serverutil')
bot.load_extension('bot.cogs.cogs')
bot.load_extension('bot.cogs.music')

bot.load_extension('bot.cogs.data.messages')
bot.load_extension('bot.cogs.data.userprofiles')
bot.load_extension('bot.cogs.data.serverref')
bot.load_extension('bot.cogs.data.dbfuncs')

bot.run(startup.read_token())
