import discord
from discord.ext import commands
import random
from datetime import datetime

class SecretSanta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Inicialização do bot
    @commands.Cog.listener()
    async def on_ready(self):
        print('Módulo SecretSanta pronto!')
    
    # COMMANDS
    @commands.command(brief=f'Ex: $secret @everyone',
        description='Manda um DM para cada membro da role, especificando seu amigo secreto.')
    @commands.has_any_role("Chefes do Role","Mestre do Role","teste alo","PseudoPiranha","Piranha")
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
    bot.add_cog(SecretSanta(bot))