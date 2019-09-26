import discord
import json

from discord.ext import commands

startup_extensions = {'cogs.prefix', 'cogs.basic', 'cogs.events', 'cogs.emoji', 'cogs.data', 'cogs.serverutil'}

prefix = '!'

def read_token():
    file = open('token.txt')
    lines = file.readlines()
    return lines[0].strip()

def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(prefix)(bot, message)

    with open("prefixes.json", 'r') as file:
        prefixes = json.load(file)
    guild_id = str(message.guild.id)

    if guild_id not in prefixes:
        return commands.when_mentioned_or(prefix)(bot, message)

    author_id = str(message.author.id)
    if author_id not in prefixes[guild_id]:
        return commands.when_mentioned_or(prefix)(bot, message)

    all_prefix = (prefixes[str(message.guild.id)][str(message.author.id)], prefix)

    return commands.when_mentioned_or(*all_prefix)(bot,message)

bot = commands.Bot(command_prefix=get_prefix)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
            continue
        print("{} loaded.".format(extension))

    bot.run(read_token())