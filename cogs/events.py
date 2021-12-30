import discord
from discord.ext import commands
import random
from datetime import datetime

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Inicialização do bot
    @commands.Cog.listener()
    async def on_ready(self):
        print('Módulo Events pronto!')

    # EVENT LISTENERS

    # TASKS


    # COMMANDS

    @commands.command(brief=f'Ex: $pairs @everyone',
        description='Gera pares aleatórios dos membros com o cargo especificado.')
    @commands.is_owner()
    @has_permissions(administrator=True, manage_server=True)
    async def pairs(self, ctx, role: discord.Role):
        nomes = [x.mention for x in role.members]
        random.shuffle(nomes)
        output = "Os casais são:"
        i = 0
        while i <= len(nomes)-2:
            output += f"\n{nomes[i]} \U00002764 {nomes[i+1]}"
            i += 2
        await ctx.send(output)
    

    @commands.command(brief=f'Ex: $secret @everyone',
        description='Manda um DM para cada membro da role, especificando seu amigo secreto.')
    @commands.is_owner()
    @has_permissions(administrator=True, manage_server=True)
    async def secret(self, ctx, role: discord.Role):
        nomes = list(role.members)
        random.shuffle(nomes)
        amigo_secreto = (nomes[0].nick if nomes[0].nick else nomes[0].name, f"{nomes[0].name}#{nomes[0].discriminator}")
        nomes.append(nomes[0])
        for user in nomes[1:]:
            name = user.nick if user.nick else user.name
            message = f"Seu amigo secreto é {amigo_secreto[1]}, AKA {amigo_secreto[0]}.\nComando executado por {ctx.author} no dia {datetime.strftime(datetime.now(),'%d/%m/%Y as %H:%M:%S (GMT +0)')}"
            amigo_secreto = (name, f"{user.name}#{user.discriminator}")
            try:
                await user.send(message)
            except:
                continue
    
def setup(bot):
    bot.add_cog(Events(bot))