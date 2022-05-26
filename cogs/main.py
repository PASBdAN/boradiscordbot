import discord
from discord.ext import commands, tasks
from database.client import Client
from itertools import cycle
import random
from datetime import datetime, timezone, timedelta

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def confirmation_react(self, ctx, msg, timeout = 20.0):
        accept =  "✅"
        decline = "❌"
        await msg.add_reaction(accept)
        await msg.add_reaction(decline)
        def check(reaction, user):
            return user == ctx.author and str(
                reaction.emoji) in [accept, decline] and reaction.message == msg
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=timeout, check=check)
            if str(reaction.emoji) == accept:
                await msg.remove_reaction(decline, msg.author)
                return True
            else:
                await msg.remove_reaction(accept, msg.author)
                return False
        except Exception as e:
            await msg.remove_reaction(decline, msg.author)
            await msg.remove_reaction(accept, msg.author)
            return False

    # EVENT LISTENERS
    @commands.Cog.listener()
    async def on_ready(self):
        db = Client('Users')
        members_list = [x for x in self.bot.get_all_members()]
        print(members_list)
        for member in members_list:
            try:
                aux = db.insert(id=member.id,name=member.name,nickname=member.display_name,created_at=datetime.now(timezone.utc))
            except Exception as e:
                db.conn.rollback()
                print(e)
        db.close_db()
        user_list = members_list# [await self.bot.fetch_user(int(y[0])) for y in db.select('id')]
        self.funny_people = [x.display_name for x in user_list]
        self.funny_emoji = ["😍","😳","😈","😏","🤫","💋","❤️","👀"]
        random.shuffle(self.funny_people)
        random.shuffle(self.funny_emoji)
        self.status_list = cycle(
            [f"ERPing with {x[0]} {x[1]}" for x in 
            list(zip(self.funny_people, cycle(self.funny_emoji))
                if len(self.funny_people) > len(self.funny_emoji)
                else zip(cycle(self.funny_people), self.funny_emoji))]
            )
        self.change_status.start()
        print('Módulo Main pronto!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db = Client('Guilds')
        prefix = db.select('prefix',id = guild.id)
        if prefix:
            db.update_by_id(id = guild.id, prefix = '$')
        else:
            db.insert(id=guild.id,prefix='$', created_at = datetime.now(timezone.utc))
        db.close_db()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        db = Client('Guilds')
        db.delete(id = guild.id)
        db.close_db()

    #TASKS
    @tasks.loop(seconds = 30)
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
        if await self.confirmation_react(ctx,msg):
            db = Client('Guilds')
            prefix_db = db.select('prefix', id = ctx.guild.id)
            if prefix_db:
                db.update_by_id(id = ctx.guild.id, prefix = prefix)
            else:
                db.insert(id = ctx.guild.id, prefix = prefix, created_at = datetime.now(timezone.utc))
            db.close_db()
            message = f'O prefixo de comandos do bot agora é {prefix}'
            await ctx.send(message)
        else:
            message = f'Tudo bem, o prefixo do bot neste servidor não mudou.'
            await ctx.send(message)
        

def setup(bot):
    bot.add_cog(Main(bot))