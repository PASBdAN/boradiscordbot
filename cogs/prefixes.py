import discord
from discord.ext import commands
from database.guilds import Guilds

class Prefixes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # EVENT LISTENERS
    @commands.Cog.listener()
    async def on_ready(self):
        print('Módulo de prefixos pronto!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guilds = Guilds()
        prefix = guilds.get_guild_value(guild.id,'prefix')
        if prefix:
            guilds.update_guild_value(guild.id,'$','prefix')
        else:
            guilds.insert_guild_value(guild.id, '$','prefix')
        guilds.close_db()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        guilds = Guilds()
        guilds.delete_guild(guild.id)
        guilds.close_db()

    #TASKS

    # COMMANDS
    @commands.command(
        brief=f'Ex: $prefix !',
        description='Troca o prefixo dos comandos do bot.')
    async def prefix(self, ctx, prefix):
        guilds = Guilds()
        # guilds.update_guild_prefix(ctx.guild.id,prefix)
        prefix_db = guilds.get_guild_value(ctx.guild.id,'prefix')
        if prefix_db:
            guilds.update_guild_value(ctx.guild.id,prefix,'prefix')
        else:
            guilds.insert_guild_value(ctx.guild.id, prefix,'prefix')
        guilds.close_db()
        message = f'O prefixo de comandos do bot agora é {prefix}'
        await ctx.send(message)

def setup(bot):
    bot.add_cog(Prefixes(bot))