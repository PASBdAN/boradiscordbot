import discord
from discord.ext import commands
import random
from datetime import datetime

class Fotografar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None

    # EVENT LISTENERS
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        self.channel = self.bot.get_channel('851446887210942484')
        # 851796006260965386
        # self.channel = self.bot.get_channel(851796006260965386)
        if reaction.message.channel.id == self.channel.id:
            print("TESTE")
            # Role = discord.utils.get(user.guild.roles, name="outro")
            Role = user.guild.get_role(926608766609289267)
            print(Role)
            await user.add_roles(Role)


    # TASKS


    # COMMANDS


def setup(bot):
    bot.add_cog(Fotografar(bot))