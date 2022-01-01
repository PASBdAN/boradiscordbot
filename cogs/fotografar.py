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
        # self.channel = self.bot.get_channel('851446887210942484')
        # 851796006260965386
        # self.channel = self.bot.get_channel(177808798117920768)
        # 888088357463285821
        # self.channel = self.bot.get_channel(888088357463285821)
        # 736746755986554951
        self.channel = self.bot.get_channel(736746755986554951)
        print(self.channel)
        if reaction.message.channel.id == self.channel.id:
            Role = user.guild.get_role(926608766609289267)
            # Role = user.guild.get_role(926942005316190289)
            print(Role)
            await user.add_roles(Role)


    # TASKS


    # COMMANDS


def setup(bot):
    bot.add_cog(Fotografar(bot))