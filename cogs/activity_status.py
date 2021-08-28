import discord
from discord.ext import commands, tasks
from itertools import cycle

ACTIVITY_STATUS_TIMER = 10

class ActivityStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_list = cycle(["Senile Scribbles Offline","Warcraft of World", "Celestial Craft 2"])

    # EVENT LISTENERS
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
        brief=f'Ex: $set_activity_timer 5',
        description='Define o intervalo em segundos entre os status de atividade do bot.')
    async def set_activity_timer(self, ctx, time: int):
        self.change_status.change_interval(seconds = time)
        self.change_status.restart()
        message = f'Atividade do bot mudará a cada {time} segundos!'
        await ctx.send(message)
    
    @commands.command(
        brief=f'Ex: $set_activity_list A1, A2, A3',
        description='Define uma lista de status de atividade do bot para serem mostrados em um loop')
    async def set_activity_list(self, ctx, *args):
        string = ' '.join(args)
        self.status_list = cycle([x.strip() for x in string.split(",")])
        self.change_status.restart()
        message = f'Lista de atividades do bot atualizada com sucesso!'
        await ctx.send(message)

def setup(bot):
    bot.add_cog(ActivityStatus(bot))
