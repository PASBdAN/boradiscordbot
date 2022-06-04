
import discord
from discord.ext import commands
import os
from database.client import Client

from manage import dict_config

BOT_KEY = dict_config['BOT_KEY']

def get_prefix(bot, message):
    db = Client('Guilds')
    server_prefix = db.select('prefix',id = message.guild.id)
    if server_prefix:
        return server_prefix[0]
    else:
        return '$'

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=get_prefix,intents=intents)


@bot.command(brief=f'Ex: $load Prefixes',
        description='Carrega o módulo especificado.')
@commands.has_permissions(manage_guild=True)
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
@commands.has_permissions(manage_guild=True)
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
@commands.has_permissions(manage_guild=True)
async def reload(ctx, extension:str):
    try:
        bot.unload_extension(f'cogs.{extension.lower()}')
        bot.load_extension(f'cogs.{extension.lower()}')
        message = f"Módulo {extension} reiniciado com sucesso!"
        await ctx.send(message)
    except Exception as e:
        message = f"Não foi possível reiniciar o módulo {extension}:\n{e}"
        await ctx.send(message)

Client().create_schema()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(BOT_KEY)