import discord
from discord.ext import commands
from database.guilds import Guilds

class Prefixes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Módulo de prefixos pronto!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guilds = Guilds()
        prefix = guilds.get_guild_prefix(guild.id)
        if prefix:
            guilds.update_guild_prefix(guild.id,'$')
        else:
            guilds.insert_guild_prefix(guild.id, '$')
        guilds.close_db()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        guilds = Guilds()
        guilds.delete_guild(guild.id)
        guilds.close_db()

    @commands.command()
    async def prefix(self, ctx, prefix):
        guilds = Guilds()
        guilds.update_guild_prefix(ctx.guild.id,prefix)
        guilds.close_db()
        message = f'O prefixo de comandos do bot agora é {prefix}'
        await ctx.send(message)

def setup(bot):
    bot.add_cog(Prefixes(bot))