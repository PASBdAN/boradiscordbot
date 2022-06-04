from asynchat import simple_producer
import asyncio
import discord
from discord import Embed
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


    async def delete_channel(self, ctx, channel, time = 60, can_cancel = False):
        if not can_cancel:
            await channel.send(f"Este canal será deletado em {time} segundos! {dia_tarde_noite().capitalize()}!")
            await sleep(time)
            await channel.delete()
            await channel.category.delete()
        else:
            msg = await channel.send(f"Este canal será deletado em {time} segundos! Deseja cancelar?")
            if await self.confirmation_react(ctx, msg, lambda : True, timeout=float(time)):
                await channel.send(f"O canal não será mais deletado! {dia_tarde_noite().capitalize()}!")
                return None
            await channel.delete()
            await channel.category.delete()
        return True


    async def confirmation_react(self, ctx, msg:discord.message, timeout = 30.0, allow_skip = False):
        accept =  "✅"
        decline = "❌"
        await msg.add_reaction(accept)
        await msg.add_reaction(decline)
        if allow_skip:
            skip = "⏭️"
            await msg.add_reaction(skip)
        def check(reaction, user):
            if allow_skip:
                return user == ctx.author and str(
                    reaction.emoji) in [accept, decline, skip] and reaction.message == msg
            return user == ctx.author and str(
                reaction.emoji) in [accept, decline] and reaction.message == msg
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=timeout, check=check)
            if str(reaction.emoji) == accept:
                await msg.remove_reaction(decline, msg.author)
                if allow_skip:
                    await msg.remove_reaction(skip, msg.author)
                return True
            elif str(reaction.emoji) == decline:
                await msg.remove_reaction(accept, msg.author)
                if allow_skip:
                    await msg.remove_reaction(skip, msg.author)
                return False
            elif str(reaction.emoji) == skip and allow_skip:
                await msg.remove_reaction(accept, msg.author)
                await msg.remove_reaction(decline, msg.author)
                return None

        except Exception as e:
            print(e)
            await msg.remove_reaction(decline, msg.author)
            await msg.remove_reaction(accept, msg.author)
            try:
                await msg.remove_reaction(skip, msg.author)
            except UnboundLocalError:
                pass
            return None


    async def create_private_channel(self, ctx):
        guild = ctx.guild
        member = ctx.author
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False), # @everyone
            member: discord.PermissionOverwrite(read_messages=True),
        }
        for role in guild.roles:
            overwrites[role] = discord.PermissionOverwrite(read_messages=False)
        category = await guild.create_category(f'datefake_{member}', overwrites=overwrites)
        return await guild.create_text_channel(f'private_chat', overwrites=overwrites, category = category)


    async def add_user_to_pool(self, ctx, channel):
        db = Client('DatefakeUsers')
        aux = db.select('user_id',user_id=ctx.author.id)
        if not aux:
            db.tb_name = 'Users'
            if not db.select(id = ctx.author.id):
                db.insert(id = ctx.author.id,display_name = ctx.author.display_name, created_at = datetime.now(timezone.utc))
            db.tb_name = 'DatefakeUsers'
            db.insert(user_id = ctx.author.id, guild_id = ctx.author.guild.id, created_at = datetime.now(timezone.utc))
            db.close_db()
            await ctx.author.add_roles(ctx.author.guild.get_role(self.role_id))
            await channel.send("Você foi adicionado na lista de participantes do evento.")
            return True


    async def remove_user_from_pool(self, ctx, channel):
        db = Client('DatefakeUsers')
        aux = db.select('user_id',user_id=ctx.author.id)
        if aux:
            db.delete(user_id=aux[0][0])
            db.close_db()
            await ctx.author.remove_roles(ctx.author.guild.get_role(self.role_id))
            await channel.send("Você foi removido da lista de participantes!")
            return True


    def create_embed(self, title:str, fields:list, colour, footer = ''):
        embed = Embed(title=title)
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.colour = colour
        embed.set_footer(text = footer)
        return embed

    async def show_participants(self, ctx, channel = None):
        db = Client('DatefakeUsers')
        datefake_users = db.select('user_id')
        db.tb_name = 'DatefakePartners'
        invites = db.select('partner_id','has_accepted')
        db.close_db()
        participants_output = ''
        status_output = ''
        for user in datefake_users:
            user_invites = [x for x in invites if x[0] == user[0]]
            invite_output = f'Já foi convidado {len(user_invites)} {"vezes" if len(user_invites) != 1 else "vez"} 🌷\n' if len(user_invites) else f'Participando do shuffle 💚\n'
            try:
                user_display_name = ctx.guild.get_member(user[0]).display_name
            except (TypeError, AttributeError):
                user_display_name = ctx.guild.fetch_member(user[0]).display_name
            participants_output += f'{user_display_name}\n'
            status_output += 'Já tem um par 💕\n' if True in [x[1] for x in user_invites] else invite_output

        embed = self.create_embed(
            # title=f'Total: {len(datefake_users)}',
            title='',
            fields=[('Participantes',participants_output,True),('Status',status_output,True)],
            colour=0xff66cc,
            footer=f'Total: {len(datefake_users)}'
        )
        if channel:
            return await channel.send(embed = embed)
        return await ctx.send(embed = embed)


    async def check_participation(self, ctx):
        db = Client('DatefakeUsers')
        aux = db.select(user_id = ctx.author.id)
        db.close_db()
        if aux:
            return True
        return False


    @commands.command(name='invite',
        brief=f'Ex: b!invite @Flakesu',
        description=f'Convida uma pessoa para ser seu par no Datefake')
    async def _invite(self, ctx, member:discord.Member):
        await ctx.message.delete()
        if member.id == ctx.author.id:
            return await ctx.author.send('Você não pode convidar você mesmo 💢😡')
        pair_id = member.id
        db = Client('DatefakeUsers')
        select = db.select(user_id = pair_id)
        db.close_db()
        if not select:
            return await ctx.author.send(f'{member.display_name} não é participante do evento ainda, você não pode convidá-lo(a) 😔')
        db = Client('DatefakePartners')
        pair_invite = db.select('datefake_id','has_accepted','has_refused', partner_id = pair_id)
        db.close_db()
        if [x for x in pair_invite if x[0] == ctx.author.id and x[2]]:
            return await ctx.author.send(f'{member.display_name} já recusou seu convite, você não pode convidá-lo(a) de novo 😔')
        elif [x for x in pair_invite if x[0] == ctx.author.id and x[1]]:
            return await ctx.author.send(f'{member.display_name} já é seu par 💕')
        elif [x for x in pair_invite if x[0] == ctx.author.id]:
            return await ctx.author.send(f'Você já convidou {member.display_name}, aguarde 🥰')
        elif True in [x[2] for x in pair_invite]:
            return await ctx.author.send(f'{member.display_name} já tem um par para o evento, você não pode convidá-lo(a) 😔')
        else:
            db = Client('DatefakePartners')
            db.insert(datefake_id = ctx.author.id, partner_id = pair_id, has_accepted = False, has_refused = False, created_at = datetime.now(timezone.utc))
            db.close_db()
            return await ctx.author.send(f'Você enviou um convite para {member.display_name}, agora é só aguardar 🥰')


    @commands.command(name='datefake',
        brief=f'Ex: b!datefake',
        description='Cria um chat privado')
    async def _datefake(self, ctx):
        # CRIANDO O CANAL PRIVADO:
        event_name = "Datefake"
        await ctx.message.delete()
        channel = await self.create_private_channel(ctx)
        await channel.send(f"{ctx.author.mention}\nEste canal é privado e será deletado em seguida.")

        # PRIMEIRO VERIFICAR SE O USUÁRIO JÁ ESTÁ PARTICIPANDO DO EVENTO:
        if not await self.check_participation(ctx):
            msg = await channel.send(f"Você deseja participar do {event_name}?")
            if await self.confirmation_react(ctx, msg):
                await self.add_user_to_pool(ctx, channel)
            else:
                await channel.send("Ok! Você não foi adicionado na lista de participantes...")
                return await self.delete_channel(ctx, channel)

        # SEGUNDO VERIFICAR SE O USUÁRIO JÁ TEM UM PAR:
        db = Client('DatefakePartners')
        user_invites = db.select('id','datefake_id','has_accepted', partner_id = ctx.author.id, has_refused = False)
        db.close_db()
        if True in [x[2] for x in user_invites]:
            try:
                user_display_name = ctx.guild.get_member([x[1] for x in user_invites if x[2]][0]).display_name
            except (TypeError, AttributeError):
                user_display_name = ctx.guild.fetch_member([x[1] for x in user_invites if x[2]][0]).display_name
            await self.show_participants(ctx, channel)
            await channel.send(f"Você já vai para o evento com 💕 {user_display_name} 💕")
            return await self.delete_channel(ctx, channel)

        # TERCEIRO VERIFICAR SE O USUÁRIO TEM CONVITES PARA VISUALIZAR:
        if user_invites:
            await channel.send(f'Você foi convidado {len(user_invites)} {"vezes" if len(user_invites) != 1 else "vez"} 📧')
            msg = await channel.send(f'Deseja responder os convites?')
            if await self.confirmation_react(ctx,msg):
                for invite in user_invites:
                    try:
                        user = ctx.guild.get_member(invite[1])
                    except (TypeError, AttributeError):
                        user = ctx.guild.fetch_member(invite[1])
                    msg = await channel.send(f'Deseja ir ao evento com {user.display_name}?')
                    react = await self.confirmation_react(ctx,msg,allow_skip=True)
                    if react:
                        db = Client('DatefakePartners')
                        db.update_by_id(id=invite[0],has_accepted=True)
                        select = db.select('id',datefake_id=ctx.author.id,partner_id=user.id)
                        if select:
                            db.update_by_id(id=select[0],has_refused=False,has_accepted=True)
                        else:
                            db.insert(datefake_id=ctx.author.id,partner_id=user.id,has_accepted=True,has_refused=False, created_at = datetime.now(timezone.utc))
                        db.close_db()
                        await user.send(f'{ctx.author.display_name} aceitou seu convite 💑')
                        await channel.send(f'{user.display_name} foi notificado via DM que você aceitou o convite. Divirtam-se 🥰')
                        await self.show_participants(ctx, channel)
                        return await self.delete_channel(ctx, channel)
                    elif react == False:
                        db = Client('DatefakePartners')
                        db.update_by_id(id=invite[0],has_refused=True)
                        db.close_db()
                    
        # QUARTO PERMITIR QUE O USUÁRIO CONVIDE ALGUEM:
        await self.show_participants(ctx, channel)
        msg = await channel.send(f"Para convidar alguém que já está participando, execute o comando  b!invite  @crush  mencionando o usuário que deseja convidar 🤩")
        return await self.delete_channel(ctx, channel)

    @commands.command(name='participants',
        brief=f'Ex: b!participants',
        description='Retorna uma lista de participantes')
    @commands.has_permissions(manage_guild=True)
    async def _participants(self, ctx):
        await self.show_participants(ctx)

def setup(bot):
    bot.add_cog(Datefake(bot))