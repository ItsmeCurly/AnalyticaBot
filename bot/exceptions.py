from discord.ext.commands.errors import CommandError
from discord.ext import commands

class AnalyticaError(CommandError):
    def __init__(self, message=None, *args):
        super().__init__(message=message, *args)
