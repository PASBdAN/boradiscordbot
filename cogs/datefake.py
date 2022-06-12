import discord
from discord import Embed
from discord.ext import commands
from datetime import datetime, timezone, timedelta
from asyncio import sleep
from database.client import Client
import asyncio
import random

import discord.utils

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
        # category = await guild.create_category(f'datefake_{member}', overwrites=overwrites)
        return await guild.create_text_channel(f'private_chat', overwrites=overwrites)#, category = category)


    async def delete_channel(self, ctx, channel, time = 60, can_cancel = False):
        if not can_cancel:
            await channel.send(f"Este canal será deletado em {time} segundos! {dia_tarde_noite().capitalize()}!")
            await sleep(time)
            await channel.delete()
            # await channel.category.delete()
        else:
            msg = await channel.send(f"Este canal será deletado em {time} segundos! Deseja cancelar?")
            if await self.confirmation_react(ctx, msg, lambda : True, timeout=float(time)):
                await channel.send(f"O canal não será mais deletado! {dia_tarde_noite().capitalize()}!")
                return None
            await channel.delete()
            # await channel.category.delete()
        return True

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


    def create_embed(self, title:str, fields:list, colour, image = None, footer = '', thumbnail = None):
        embed = Embed(title=title)
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        if image:
            embed.set_image(url=image)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        embed.colour = colour
        embed.set_footer(text = footer)
        return embed

    async def next_page(self, ctx, datefake_users, pages, pagination, invites, msg):
        current_page = 0
        left = "⬅️"
        right = "➡️"
        await msg.add_reaction(left)
        await msg.add_reaction(right)
        def check(reaction, user):
            return user == ctx.author and str(
                reaction.emoji) in [left, right] and reaction.message == msg
                
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                if str(reaction.emoji) == left:
                    print('left')
                    if current_page <= 0:
                        current_page = len(datefake_users)/pagination - 1
                        if str(current_page).split('.')[1] != '0':
                            current_page = int(current_page) + 1
                        else:
                            current_page = int(current_page)
                    else:
                        current_page -= 1
                    print(current_page)
                    participants_output = ''
                    status_output = ''
                    print(f'{current_page*pagination}:{(current_page+1)*pagination}')
                    for user in datefake_users[current_page*pagination:(current_page+1)*pagination]:
                        # print(user)
                        user_invites = [x for x in invites if x[0] == user[0] and not x[2]]
                        invite_output = f'Participando do shuffle, recebeu {len(user_invites)} {"convites" if len(user_invites) != 1 else "convite"} 🌷\n' if len(user_invites) else f'Participando do shuffle 💚\n'
                        try:
                            user_display_name = ctx.guild.get_member(user[0]).display_name
                        except (TypeError, AttributeError):
                            user_display_name = await ctx.guild.fetch_member(user[0]).display_name
                        participants_output += f'{user_display_name}\n'
                        status_output += 'Já tem um par 💕\n' if True in [x[1] for x in user_invites] else invite_output
                    print(participants_output)
                    print(status_output)
                    await msg.edit(embed = self.create_embed(
                        title=f'Total de participantes: {len(datefake_users)}',
                        fields=[('Participantes',participants_output,True),('Status',status_output,True)],
                        colour=0xff66cc,
                        footer=f'Página {(current_page) + 1}/{pages}'))

                if str(reaction.emoji) == right:
                    print('right')
                    if current_page*pagination >= len(datefake_users) - pagination:
                        current_page = 0
                    else:
                        current_page += 1

                    participants_output = ''
                    status_output = ''
                    
                    for user in datefake_users[current_page*pagination:(current_page+1)*pagination]:
                        user_invites = [x for x in invites if x[0] == user[0] and not x[2]]
                        invite_output = f'Participando do shuffle, recebeu {len(user_invites)} {"convites" if len(user_invites) != 1 else "convite"} 🌷\n' if len(user_invites) else f'Participando do shuffle 💚\n'
                        try:
                            user_display_name = ctx.guild.get_member(user[0]).display_name
                        except (TypeError, AttributeError):
                            user_display_name = await ctx.guild.fetch_member(user[0]).display_name
                        participants_output += f'{user_display_name}\n'
                        status_output += 'Já tem um par 💕\n' if True in [x[1] for x in user_invites] else invite_output

                    await msg.edit(embed = self.create_embed(
                        title=f'Total de participantes: {len(datefake_users)}',
                        fields=[('Participantes',participants_output,True),('Status',status_output,True)],
                        colour=0xff66cc,
                        footer=f'Página {(current_page) + 1}/{pages}'))

            except asyncio.TimeoutError:
                break

    async def show_participants(self, ctx, channel = None):
        db = Client('DatefakeUsers')
        datefake_users = db.select('user_id')
        db.tb_name = 'DatefakePartners'
        invites = db.select('partner_id','has_accepted', 'has_refused')
        db.close_db()

        participants_output = ''
        status_output = ''

        pagination = 20
        pages = len(datefake_users)/pagination
        if str(pages).split('.')[1] != '0':
            pages = int(pages) + 1
        else:
            pages = int(pages)
        print(pages)
        print(pagination, len(datefake_users))
        current_page = 0

        for user in datefake_users[current_page*pagination:(current_page+1)*pagination]:
            user_invites = [x for x in invites if x[0] == user[0] and x[2] == False]
            invite_output = f'Participando do shuffle, recebeu {len(user_invites)} {"convites" if len(user_invites) != 1 else "convite"} 🌷\n' if len(user_invites) else f'Participando do shuffle 💚\n'
            try:
                user_display_name = ctx.guild.get_member(user[0]).display_name
            except (TypeError, AttributeError):
                user_display_name = await ctx.guild.fetch_member(user[0]).display_name
            participants_output += f'{user_display_name}\n'
            status_output += 'Já tem um par 💕\n' if True in [x[1] for x in user_invites] else invite_output

        embed = self.create_embed(
            title=f'Total de participantes: {len(datefake_users)}',
            fields=[('Participantes',participants_output,True),('Status',status_output,True)],
            colour=0xff66cc,
            footer=f'Página {(current_page) + 1}/{pages}'
        )

        if channel:
            msg = await channel.send(embed = embed)
        else:
            msg = await ctx.send(embed = embed)
        if pagination < len(datefake_users):
            asyncio.ensure_future(self.next_page(ctx,datefake_users,pages,pagination,invites,msg))


    async def check_participation(self, ctx):
        db = Client('DatefakeUsers')
        aux = db.select(user_id = ctx.author.id)
        db.close_db()
        if aux:
            return True
        return False


    @commands.command(name='undo_pair',
        brief='Ex: b!undo_pair @Flakesu',
        description='Desfaz um par e manda uma dm para ambos avisando')
    @commands.has_permissions(manage_guild=True)
    async def _undo_pair(self,ctx,member:discord.Member):
        db = Client('DatefakeUsers')
        select = db.select(user_id = member.id)
        db.close_db()
        if not select:
            return await ctx.send(f'{member.display_name} não participa do evento.')
        db = Client('DatefakePartners')
        select = db.select('id','partner_id',datefake_id=member.id,has_accepted=True)
        db.close_db()
        if select:
            try:
                pair = ctx.guild.get_member(select[0][1])
            except (TypeError, AttributeError):
                pair = await ctx.guild.fetch_member(select[0][1])
            msg = await ctx.send(f'Deseja desfazer o par {member.display_name} x {pair.display_name}?')
            if await self.confirmation_react(ctx,msg):
                db = Client('DatefakePartners')
                db.update_by_id(datefake_id=pair.id,has_accepted=False,has_refused=True)
                db.update_by_id(datefake_id=member.id,has_accepted=False,has_refused=True)
                db.close_db()
                return await ctx.send(f'Par desfeito!')
            return await ctx.send(f'Ok! O par não foi alterado.')
        return await ctx.send(f'O usuário {member.display_name} não tem nenhum par.')


    @commands.command(name='invite',
        brief=f'Ex: b!invite Flakesu',
        description=f'Convida uma pessoa para ser seu par no Datefake')
    async def _invite(self, ctx, *member):
        await ctx.message.delete()
        member = ' '.join(member)
        try:
            member = await commands.converter.MemberConverter().convert(ctx,member)
        except Exception as e:
            print(e)
            return await ctx.send(f'Usuário {member} não foi encontrado, verifique se tem emojis ou letras maiúsculas no nome do usuário e tente novamente.')
        if member.id == ctx.author.id:
            return await ctx.send('Você não pode convidar você mesmo 💢😡')
        msg = await ctx.send(embed = self.create_embed(
            member.display_name,
            [],
            0xff66cc,
            member.avatar_url,
            'Deseja convidar este usuário?'
        ))
        if not await self.confirmation_react(ctx,msg):
            await msg.delete()
            return await ctx.send(f'Ok, o usuário {member.display_name} não foi convidado!')
        await msg.delete()
        pair_id = member.id
        db = Client('DatefakeUsers')
        select = db.select(user_id = pair_id)
        db.close_db()
        if not select:
            try:
                return await ctx.author.send(f'{member.display_name} não é participante do evento ainda, você não pode convidá-lo(a) 😔')
            except:
                return await ctx.send(f'{member.display_name} não é participante do evento ainda, você não pode convidá-lo(a) 😔')
        db = Client('DatefakePartners')
        self_invite = db.select('partner_id',datefake_id=ctx.author.id,has_accepted = True)
        if self_invite:
            try:
                user_display_name = ctx.guild.get_member(self_invite[0][0]).display_name
            except (TypeError, AttributeError):
                user_display_name = await ctx.guild.fetch_member(self_invite[0][0]).display_name
            db.close_db()
            try:
                return await ctx.author.send(f'Você já vai ao eventos com {user_display_name}, não pode convidar mais pessoas 🤭')
            except:
                return await ctx.send(f'Você já vai ao eventos com {user_display_name}, não pode convidar mais pessoas 🤭')
        pair_invite = db.select('datefake_id','has_accepted','has_refused', partner_id = pair_id)
        db.close_db()
        if [x for x in pair_invite if x[0] == ctx.author.id and x[2]]:
            try:
                return await ctx.author.send(f'{member.display_name} já recusou seu convite, você não pode convidá-lo(a) de novo 😔')
            except:
                return await ctx.send(f'Você já vai ao eventos com {user_display_name}, não pode convidar mais pessoas 🤭')
        elif [x for x in pair_invite if x[0] == ctx.author.id and x[1]]:
            try:
                return await ctx.author.send(f'{member.display_name} já é seu par 💕')
            except:
                return await ctx.send(f'{member.display_name} já é seu par 💕')
        elif [x for x in pair_invite if x[0] == ctx.author.id]:
            try:
                return await ctx.author.send(f'Você já convidou {member.display_name}, aguarde 🥰')
            except:
                return await ctx.send(f'Você já convidou {member.display_name}, aguarde 🥰')
        elif True in [x[1] for x in pair_invite]:
            try:
                return await ctx.author.send(f'{member.display_name} já tem um par para o evento, você não pode convidá-lo(a) 😔')
            except:
                return await ctx.send(f'{member.display_name} já tem um par para o evento, você não pode convidá-lo(a) 😔')
        else:
            db = Client('DatefakePartners')
            db.insert(datefake_id = ctx.author.id, partner_id = pair_id, has_accepted = False, has_refused = False, created_at = datetime.now(timezone.utc))
            db.close_db()
            try: 
                return await ctx.author.send(f'Você enviou um convite para {member.display_name}, agora é só aguardar 🥰')
            except:
                return await ctx.send(f'Você enviou um convite para {member.display_name}, agora é só aguardar 🥰')

    def get_partners(self, partners_dict:dict) -> list:
        lista = []
        for key in list(partners_dict.keys())[::2]:
            lista.append(key)
            lista.append(partners_dict[key])
        return lista

    async def random_pairs(self, members) -> list:
        nomes = [x.display_name for x in members]
        random.shuffle(nomes)
        i = 0
        left_output = ''
        right_output = ''
        while i <= len(nomes)-2:
            left_output += f'\n{nomes[i]}'
            right_output += f'\n{nomes[i+1]}'
            i += 2
        return left_output, right_output

    async def pairs(self, members):
        nomes = [x.display_name for x in members]
        output = ""
        i = 0
        left_output = ''
        right_output = ''
        while i <= len(nomes)-2:
            left_output += f'\n{nomes[i]}'
            right_output += f'\n{nomes[i+1]}'
            i += 2
        return left_output, right_output

    @commands.command(name='shuffle',
        brief=f'Ex: b!shuffle',
        description='Cria um chat privado')
    @commands.has_permissions(manage_guild=True)
    async def _shuffle(self, ctx):
        db = Client('DatefakeUsers')
        datefake_users = db.select('user_id')
        db.tb_name = 'DatefakePartners'
        datefake_partners = db.select('datefake_id','partner_id',has_accepted=True)
        db.close_db()

        shuffle_ids = [x[0] for x in datefake_users if x[0] not in [x[0] for x in datefake_partners]]
        shuffle_members = []
        for id in shuffle_ids:
            try:
                member = ctx.guild.get_member(id)
            except (TypeError, AttributeError):
                member = await ctx.guild.fetch_member(id)
            shuffle_members.append(member)

        pairs_ids = self.get_partners(dict(datefake_partners))
        pairs_members = []
        for id in pairs_ids:
            try:
                member = ctx.guild.get_member(id)
            except (TypeError, AttributeError):
                member = await ctx.guild.fetch_member(id)
            pairs_members.append(member)

        shuffle_left, shuffle_right = await self.random_pairs(shuffle_members)
        embed = self.create_embed(
            title=f'Pares gerados do shuffle',
            fields=[
                (f"{'💚'*11}",shuffle_left,True),
                (f"{'💙'*11}",shuffle_right,True)],
            colour=0xf542ad
            # footer=f'Página {(current_page) + 1}/{pages}'
        )
        await ctx.send(embed = embed)

        pairs_left, pairs_right = await self.pairs(pairs_members)
        embed = self.create_embed(
            title=f'Pares formados por invites',
            fields=[
                (f"{'💚'*11}",pairs_left,True),
                (f"{'💙'*11}",pairs_right,True)
            ],
            colour=0x42b3f5
            # footer=f'Página {(current_page) + 1}/{pages}'
        )
        await ctx.send(embed = embed)

    @commands.command(name='datefake',
        brief=f'Ex: b!datefake',
        description='Cria um chat privado')
    @commands.has_permissions(manage_guild=True)
    async def _datefake(self, ctx):
        # CRIANDO O CANAL PRIVADO:
        event_name = "Datefake"
        await ctx.message.delete()
        channel = await self.create_private_channel(ctx)
        await channel.send(f"{ctx.author.mention}\nEste canal é privado e será deletado em seguida.")

        # PRIMEIRO VERIFICAR SE O USUÁRIO JÁ ESTÁ PARTICIPANDO DO EVENTO:
        if not await self.check_participation(ctx):
            db = Client('DatefakeUsers')
            participants = db.select()
            db.close_db()
            if len(participants) >= 60:
                msg = await channel.send(f"Sinto muito, o evento já está na máxima capacidade de participantes 😔")
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
                user_display_name = await ctx.guild.fetch_member([x[1] for x in user_invites if x[2]][0]).display_name
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
                        user = await ctx.guild.fetch_member(invite[1])
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
                        try:
                            await user.send(f'{ctx.author.display_name} aceitou seu convite 💑')
                            await channel.send(f'{user.display_name} foi notificado via DM que você aceitou o convite. Divirtam-se 🥰')
                        except:
                            await channel.send(f' {user.display_name} desabilitou DMs do server então não pude notifica-lo(a) do aceite, mas os dois já são pares. Divirtam-se 🥰')
                        await self.show_participants(ctx, channel)
                        return await self.delete_channel(ctx, channel)
                    elif react == False:
                        db = Client('DatefakePartners')
                        db.update_by_id(id=invite[0],has_refused=True)
                        db.close_db()
                    
        # QUARTO PERMITIR QUE O USUÁRIO CONVIDE ALGUEM:
        await self.show_participants(ctx, channel)
        msg = await channel.send(f"Para convidar alguém que já está participando, execute o comando  b!invite user  escrevendo o nickname, id ou nome#discriminador do usuário que você quer convidar 🤩")
        return await self.delete_channel(ctx, channel)

    @commands.command(name='participants',
        brief=f'Ex: b!participants',
        description='Retorna uma lista de participantes')
    @commands.has_permissions(manage_guild=True)
    async def _participants(self, ctx):
        await self.show_participants(ctx)

def setup(bot):
    bot.add_cog(Datefake(bot))