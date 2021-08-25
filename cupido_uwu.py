
import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='&',intents=intents)

'''
@bot.command()
async def pairs(ctx, *args):
    string = ' '.join(args)
    nomes = [x.strip() for x in string.split(",")]
    random.shuffle(nomes)
    output = "Os casais são:"
    i = 0
    while i <= len(nomes)-2:
        output += f"\n{nomes[i]} \U00002764 {nomes[i+1]}"
        i += 2
    await ctx.send(output)
'''

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

bot.run('LKzaWwEJpMgnX_36qJbSfmGdA_5LkH4m')