import discord
from discord.ext import commands

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # EVENT LISTENERS
    # TASKS
    # COMMANDS
def setup(bot):
    bot.add_cog(Currency(bot))