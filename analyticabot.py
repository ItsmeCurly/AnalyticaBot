import discord, json, configparser, six, utils.startup as startup
from discord.ext import commands

CONFIG_PATH = 'static_config.ini'

class AnalyticaBot(commands.Bot):
    def __init__(self, *args, debug=False, **kwargs):
        commands.Bot.__init__(self, self.init_prefix)
        self.startup_extensions = {'cogs.prefix', 'cogs.basic',
                                   'cogs.events', 'cogs.emoji',
                                   'cogs.data', 'cogs.serverutil'}
        self.prefix = '!'

        startup.main()
        self.init_cogs()

        self._run()

    def init_cogs(self):
        for extension in self.startup_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                exc = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {extension}\n{exc}')
                continue
            print("{} loaded.".format(extension))

    def init_prefix(self, bot, message):
        if not message.guild:
            return commands.when_mentioned_or(self.prefix)(self, message)

        with open("prefixes.json", 'r') as file:
            prefixes = json.load(file)
        guild_id = str(message.guild.id)

        if guild_id not in prefixes:
            return commands.when_mentioned_or(self.prefix)(self, message)

        author_id = str(message.author.id)
        if author_id not in prefixes[guild_id]:
            return commands.when_mentioned_or(self.prefix)(self, message)

        all_prefix = (prefixes[str(message.guild.id)]
                      [str(message.author.id)], self.prefix)

        return commands.when_mentioned_or(*all_prefix)(self, message)

    def read_token(self):
        config_path = get_config_file_at_path(CONFIG_PATH)

        token_config_file_path = config_path['Files']['config_path']
        token_config = get_config_file_at_path(token_config_file_path)

        return token_config['Token']['token']

    def _run(self):
        self.run(self.read_token())

def get_config_file_at_path(path: str) -> configparser:
    cfg = configparser.ConfigParser()
    cfg.read(path)
    return cfg

if __name__ == "__main__":
    AnalyticaBot()