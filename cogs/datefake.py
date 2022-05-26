import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta
from asyncio import sleep
from database.client import Client

def dia_tarde_noite():
    timezone_offset = -3.0  # São Paulo (UTC−03:00)
    tzinfo = timezone(timedelta(hours=timezone_offset))
    hour = int(datetime.now(tzinfo).hour)
    if hour >= 5 and hour < 12:
        return "bom dia"
    elif hour >= 12 and hour < 18:
        return "boa tarde"
    else:
        return "boa noite"

class Datefake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.module_name = "Datefake"
        self.role_id = 978153725711503430
        # self.role_id = 978155909987577876 # server de teste

    # Inicialização do bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Módulo {self.module_name} pronto!')


    async def delete_channel(self, ctx, channel, time = 10, can_cancel = False):
        if not can_cancel:
            await channel.send(f"Este canal será deletado em {time} segundos! {dia_tarde_noite().capitalize()}!")
            await sleep(10)
            await channel.delete()
        else:
            msg = await channel.send(f"Este canal será deletado em {time} segundos! Deseja cancelar?")
            if await self.confirmation_react(ctx, msg, lambda : True, timeout=10.0):
                await channel.send(f"O canal não será mais deletado! {dia_tarde_noite().capitalize()}!")
                return None
            await channel.delete()
        return True


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


    async def create_private_channel(self, ctx):
        guild = ctx.guild
        member = ctx.author
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False), # @everyone
            member: discord.PermissionOverwrite(read_messages=True),
        }
        for role in guild.roles:
            overwrites[role] = discord.PermissionOverwrite(read_messages=False)
        return await guild.create_text_channel(f'datefake_{member}', overwrites=overwrites)


    async def add_user_to_pool(self, ctx, channel):
        db = Client('Datefake')
        aux = db.select('id',user_id=ctx.author.id)
        if not aux:
            db.tb_name = 'Users'
            if not db.select(id = ctx.author.id):
                db.insert(id = ctx.author.id, name = ctx.author.name, nickname = ctx.author.display_name, created_at = datetime.now(timezone.utc))
            db.tb_name = 'Datefake'
            db.insert(user_id = ctx.author.id, guild_id = ctx.author.guild.id, created_at = datetime.now(timezone.utc))
            db.close_db()
            await ctx.author.add_roles(ctx.author.guild.get_role(self.role_id))
            await channel.send("Você foi adicionado na lista de participantes do evento.")
            return True


    async def remove_user_from_pool(self, ctx, channel):
        db = Client('Datefake')
        aux = db.select('id',user_id=ctx.author.id)
        if aux:
            db.delete(id=aux[0][0])
            db.close_db()
            await ctx.author.remove_roles(ctx.author.guild.get_role(self.role_id))
            await channel.send("Você foi removido da lista de participantes!")
            return True
        

    async def check_participation(self, ctx):
        db = Client('Datefake')
        aux = db.select(user_id = ctx.author.id)
        db.close_db()
        if aux:
            return True
        return False


    @commands.command(name='datefake',
        brief=f'Ex: $datefake',
        description='Cria um chat privado')
    async def _datefake(self, ctx):
        event_name = "Datefake"
        await ctx.message.delete()
        channel = await self.create_private_channel(ctx)
        await channel.send(f"{ctx.author.mention}\nEste canal é privado e será deletado em seguida.")

        if await self.check_participation(ctx):
            msg = await channel.send(f"Você já é participante do {event_name}! Deseja sair do evento?")
            confirmation = await self.confirmation_react(ctx, msg)
            if confirmation:
                await self.remove_user_from_pool(ctx, channel)
                return await self.delete_channel(ctx, channel)
            else:
                await channel.send("Ok! Você ainda é um participante do evento!")
                return await self.delete_channel(ctx, channel)

        msg = await channel.send(f"Você deseja participar do {event_name}?")
        confirmation = await self.confirmation_react(ctx, msg)
        if confirmation:
            await self.add_user_to_pool(ctx, channel)
            return await self.delete_channel(ctx, channel)
        else:
            await channel.send("Ok! Você não foi adicionado na lista de participantes...")
            return await self.delete_channel(ctx, channel)


    @commands.command(name='participants',
        brief=f'Ex: $participants',
        description='Retorna uma lista de participantes')
    @commands.has_permissions(manage_guild=True)
    async def _participants(self, ctx):
        db = Client('Datefake')
        users_list = [ctx.guild.get_member(y[0]).display_name for y in db.select('user_id')]
        db.close_db()
        output = f'Total de participantes: {len(users_list)}'
        for user in users_list:
            output += f'\n{user}'
        await ctx.send(output)

def setup(bot):
    bot.add_cog(Datefake(bot))