import discord
import json
import configparser
import six
import bot.utils.startup as startup

from bot.utils.prefix import get_prefix
from discord.ext import commands

startup.main()

bot = commands.Bot(command_prefix=get_prefix,
                   case_insensitive = True,
                   activity = discord.Game("halp me"))

bot.load_extension('bot.cogs.prefix')
bot.load_extension('bot.cogs.basic')
bot.load_extension('bot.cogs.events')
bot.load_extension('bot.cogs.emoji')
bot.load_extension('bot.cogs.data')
bot.load_extension('bot.cogs.serverutil')
bot.load_extension('bot.cogs.cogs')

bot.run(startup.read_token())