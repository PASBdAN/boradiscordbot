import discord
from discord.ext import commands
import random

class DateFake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Inicialização do bot
    @commands.Cog.listener()
    async def on_ready(self):
        print('Módulo DateFake pronto!')
    
    # COMMANDS
    @commands.command(brief=f'Ex: $pairs @everyone',
        description='Gera pares aleatórios dos membros com o cargo especificado.')
    @commands.has_any_role("Chefes do Role","Mestre do Role","teste alo","PseudoPiranha")
    async def pairs(self, ctx, role: discord.Role):
        nomes = [x.mention for x in role.members]
        random.shuffle(nomes)
        output = "Os casais são:"
        i = 0
        while i <= len(nomes)-2:
            output += f"\n{nomes[i]} \U00002764 {nomes[i+1]}"
            i += 2
        await ctx.send(output)

def setup(bot):
    bot.add_cog(DateFake(bot))