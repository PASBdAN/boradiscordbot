import discord
from discord.ext import commands, tasks
from discord import Embed
from database.guilds import Guilds
from database.users import Users
from itertools import cycle
import random

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.funny_people = ["Flakesu","Erediin","Tarado","Ciri","Castell","Reninha","InsaneCat",
    "Anezaki","ThePearl","Shizu","Bubbles","Kalmorph","SirT","JulieVR","Miami","Tag",
    "Cautelosa","Coisinha","Biscate"]
        self.funny_emoji = ["😍","😳","😈","😏","🤫","💋","❤️","👀"]
        random.shuffle(self.funny_people)
        random.shuffle(self.funny_emoji)
        self.status_list = cycle(
            [f"ERPing with {x[0]} {x[1]}" for x in 
            list(zip(self.funny_people, cycle(self.funny_emoji))
                if len(self.funny_people) > len(self.funny_emoji)
                else zip(cycle(self.funny_people), self.funny_emoji))]
            )

    # EVENT LISTENERS
    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print('Módulo Main pronto!')

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
    @tasks.loop(seconds = 60)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.status_list)))


    # COMMANDS

    @commands.command(
        name="prefix",
        brief=f'Ex: $prefix !',
        description='Troca o prefixo dos comandos do bot.')
    @commands.has_permissions(manage_guild=True)
    async def _prefix(self, ctx, prefix):
        msg = await ctx.send(f'Deseja mesmo atualizar o prefixo para <{prefix}> ?')
        accept =  "✅"
        decline = "❌"
        await msg.add_reaction(accept)
        await msg.add_reaction(decline)
        def check(reaction, user):
            return user == ctx.author and str(
                reaction.emoji) in [accept, decline] and reaction.message == msg
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10.0, check=check)
            if str(reaction.emoji) == accept:
                guilds = Guilds()
                prefix_db = guilds.get_guild_value(ctx.guild.id, 'prefix')
                if prefix_db:
                    guilds.update_guild_value(ctx.guild.id, prefix, 'prefix')
                else:
                    guilds.insert_guild_value(ctx.guild.id, prefix, 'prefix')
                guilds.close_db()
                message = f'O prefixo de comandos do bot agora é {prefix}'
                await ctx.send(message)
            elif str(reaction.emoji) == decline:
                message = f'Tudo bem, o prefixo do bot neste servidor não mudou.'
                await ctx.send(message)
        except:
            message = f'Ocorreu um erro ao processar o comando :('
            await ctx.send(message)
    

    @commands.command(
        brief=f'Ex: $set_activity_timer 5',
        description='Define o intervalo em segundos entre os status de atividade do bot.')
    @commands.has_permissions(manage_guild=True)
    async def set_activity_timer(self, ctx, time: int):
        self.change_status.change_interval(seconds = time)
        self.change_status.restart()
        message = f'Atividade do bot mudará a cada {time} segundos!'
        await ctx.send(message)
    

    @commands.command(
        brief=f'Ex: $set_activity_list A1, A2, A3',
        description='Define uma lista de status de atividade do bot para serem mostrados em um loop')
    @commands.has_permissions(manage_guild=True)
    async def set_activity_list(self, ctx, *args):
        string = ' '.join(args)
        self.status_list = cycle([x.strip() for x in string.split(",")])
        self.change_status.restart()
        message = f'Lista de atividades do bot atualizada com sucesso!'
        await ctx.send(message)


    @commands.command(
        name='dbsync',
        brief=f'Ex: $dbsync',
        description='Pega todas as informações relevantes do servidor e seus membros e salva no banco')
    @commands.has_permissions(administrator=True)
    async def dbsync(self, ctx):
        users = Users()
        for member in ctx.guild.members:
            name = users.get_user_value(member.id,'name')
            if name or name != member.name:
                users.update_user_value(member.id,member.name,'name')
            else:
                users.insert_user_value(member.id, member.name,'name')
        users.close_db()

    
    @commands.command(
        name='user',
        brief=f'Ex: $user @crush',
        description='Verifica se o usuário está registrado no banco')
    @commands.has_permissions(manage_guild=True)
    async def get_user(self, ctx, member: discord.Member):
        users = Users()
        name = users.get_user_value(member.id,'name')
        if name:
            message = f'O usuário {member.nick} está registrado no banco!'
        else:
            message = f'O usuário não foi encontrado no banco.'
        await ctx.send(message)
        

def setup(bot):
    bot.add_cog(Main(bot))