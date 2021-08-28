
import discord
from discord.ext import commands
import os
import random
from database.guilds import Guilds

def get_prefix(bot, message):
    server_prefix = []
    guilds = Guilds()
    server_prefix = guilds.get_guild_prefix(message.guild.id)
    if server_prefix:
        return server_prefix[0]
    else:
        return '$'

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=get_prefix,intents=intents)

@bot.command(brief=f'Ex: $load Prefixes',
        description='Carrega o módulo especificado.')
async def load(ctx, extension:str):
    try:
        bot.load_extension(f'cogs.{extension.lower()}')
        message = f"Módulo {extension} carregado com sucesso"
        await ctx.send(message)
    except Exception as e:
        message = f"Não foi possível carregar o módulo {extension}:\n{e}"
        await ctx.send(message)

@bot.command(brief=f'Ex: $unload Prefixes',
        description='Desativa o módulo especificado.')
async def unload(ctx, extension:str):
    message = ""
    try:
        bot.unload_extension(f'cogs.{extension.lower()}')
        message = f"Módulo {extension} desativado com sucesso!"
        await ctx.send(message)
    except Exception as e:
        message = f"Não foi possível desativar o módulo {extension}:\n{e}"
        await ctx.send(message)

@bot.command(brief=f'Ex: $reload Prefixes',
        description='Restarta o módulo especificado.')
async def reload(ctx, extension:str):
    try:
        bot.unload_extension(f'cogs.{extension.lower()}')
        bot.load_extension(f'cogs.{extension}')
        message = f"Módulo {extension} reiniciado com sucesso!"
        await ctx.send(message)
    except Exception as e:
        message = f"Não foi possível reiniciar o módulo {extension}:\n{e}"
        await ctx.send(message)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command()
async def pairs(ctx, role: discord.Role):
    nomes = [x.mention for x in role.members]
    random.shuffle(nomes)
    output = "Os casais são:"
    i = 0
    while i <= len(nomes)-2:
        output += f"\n{nomes[i]} \U00002764 {nomes[i+1]}"
        i += 2
    await ctx.send(output)

# bot.run('ODUxNTg1MDAwNTAzOTAyMjE4.YL6aVQ.4tzJbf6OAftDJ8MmJO435sjmuNE')
bot.run('ODYzNTIxODIzMjYyMzc1OTk4.YOoHXg.C-jh4M8sg4SJRv-wYSRkdUA4plg')