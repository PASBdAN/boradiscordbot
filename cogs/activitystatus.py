import discord
from discord.ext import commands, tasks
from itertools import cycle
from database.guilds import Guilds

ACTIVITY_STATUS_TIMER = 10

class ActivityStatus(commands.Cog):
    def __init__(self, bot):
        activity_list = ['VRChat']
        self.bot = bot
        self.status_list = cycle(activity_list)
        self.activity_timer = 10

    # EVENT LISTENERS
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guilds = Guilds()
        activity = guilds.get_guild_value(guild.id, 'activity')
        if activity:
            guilds.update_guild_value(guild.id,'VRChat','activity')
        else:
            guilds.insert_guild_value(guild.id, 'VRChat','activity')
            
        activity_timer = guilds.get_guild_value(guild.id, 'activity_timer')
        if activity_timer:
            guilds.update_guild_value(guild.id,10,'activity_timer')
        else:
            guilds.insert_guild_value(guild.id,10,'activity_timer')
        guilds.close_db()

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print('Módulo de atividade pronto!')
        

    # TASKS
    @tasks.loop(seconds = ACTIVITY_STATUS_TIMER)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.status_list)))

    # COMMANDS
    @commands.command(
        brief=f'Ex: $activity_timer 5',
        description='Define o intervalo em segundos entre os status de atividade do bot.')
    async def activity_timer(self, ctx, time: int):
        guilds = Guilds()
        guilds.update_guild_value(ctx.guild.id,time,'activity_timer')
        guilds.close_db()
        self.change_status.change_interval(seconds = time)
        self.change_status.restart()
        message = f'Atividade do bot mudará a cada {time} segundos!'
        await ctx.send(message)
    
    @commands.command(
        brief=f'Ex: $activity VRChat, Bananas, Your Mom',
        description='Define uma lista de status de atividade do bot para serem mostrados em um loop')
    async def activity(self, ctx, *args):
        guilds = Guilds()
        string = ' '.join(args)
        guilds.update_guild_value(ctx.guild.id,string,'activity_timer')
        guilds.close_db()
        self.status_list = cycle([x.strip() for x in string.split(",")])
        self.change_status.restart()
        message = f'Lista de atividades do bot atualizada com sucesso!'
        await ctx.send(message)

def setup(bot):
    bot.add_cog(ActivityStatus(bot))
