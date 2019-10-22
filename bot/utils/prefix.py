import discord
import json

from discord.ext import commands
from bot.constants import DEFAULT_PREFIX

def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)

    with open("prefixes.json", 'r') as file:
        prefixes = json.load(file)
    guild_id = str(message.guild.id)

    if guild_id not in prefixes:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)

    author_id = str(message.author.id)
    if author_id not in prefixes[guild_id]:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)

    all_prefix = (prefixes[str(message.guild.id)]
                  [str(message.author.id)], DEFAULT_PREFIX)

    return commands.when_mentioned_or(*all_prefix)(bot, message)
