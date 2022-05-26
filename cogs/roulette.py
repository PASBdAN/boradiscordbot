import discord
from discord.ext import commands
# from database.events import Events as GuildEvents
import random
from datetime import datetime# , timezone


class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.module_name = "Events"

    # Inicialização do bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Módulo {self.module_name} pronto!')


def setup(bot):
    bot.add_cog(Roulette(bot))