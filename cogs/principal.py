import discord
from discord.ext import commands

class Principal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Inicialização do bot
    @commands.Cog.listener()
    async def on_ready(self):
        print('Módulo principal pronto!')

def setup(bot):
    bot.add_cog(Principal(bot))
