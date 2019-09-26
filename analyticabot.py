""" import discord, json
from discord.ext import commands
    
class AnalyticaBot(commands.Bot):
    def __init__(self, *args, debug=False, **kwargs):
        #super.__init__(*args,
        self.startup_extensions = {'cogs.prefix', 'cogs.basic',
                                   'cogs.events', 'cogs.emoji', 'cogs.data', 'cogs.serverutil'}
        self.prefix = '!'
        pass
    
    def init_cogs(self):
        for extension in self.startup_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))
                continue
            print("{} loaded.".format(extension))

    def init_prefix(self, message):
        if not message.guild:
            return commands.when_mentioned_or(prefix)(self, message)

        with open("prefixes.json", 'r') as file:
            prefixes = json.load(file)
        guild_id = str(message.guild.id)

        if guild_id not in prefixes:
            return commands.when_mentioned_or(prefix)(self, message)

        author_id = str(message.author.id)
        if author_id not in prefixes[guild_id]:
            return commands.when_mentioned_or(prefix)(self, message)

        all_prefix = (prefixes[str(message.guild.id)]
                    [str(message.author.id)], prefix)

        return commands.when_mentioned_or(*all_prefix)(self, message)
    def init_dbs(self):
        pass
    def init_token(self):
        file = open('token.txt')
        lines = file.readlines()
        return lines[0].strip()
    def run(self):
        bot = commands.Bot(command_prefix=init_prefix(self))
        bot.run(read_token())
 """