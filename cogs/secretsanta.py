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
    async def secret(self, ctx, role: discord.Role):
        nomes = list(role.members)
        random.shuffle(nomes)
        amigo_secreto = (nomes[0].nick if nomes[0].nick else nomes[0].name, f"{nomes[0].name}#{nomes[0].discriminator}")
        nomes.append(nomes[0])
        for user in nomes[1:]:
            name = user.nick if user.nick else user.name
            message = f"Seu amigo secreto é {amigo_secreto[1]}, AKA {amigo_secreto[0]}.Sorteio feito em: {datetime.strftime(datetime.now(),'%d/%m/%Y %H:%M:%S')}, pelo usuário {ctx.author}"
            amigo_secreto = (name, f"{user.name}#{user.discriminator}")
            try:
                await user.send(message)
            except:
                continue

def setup(bot):
    bot.add_cog(SecretSanta(bot))