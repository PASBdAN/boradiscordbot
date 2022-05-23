import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta
from asyncio import sleep
from database.users import Users

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

    async def invite_pair(self, ctx, channel):
        await channel.send("Marque neste chat quem é a pessoa que você deseja convidar. Ex: @crush")
        await channel.send("OBS: A pessoa será adicionada neste chat para confirmar. Fale com ela antes pelo amor de deus.")
        return None

    async def add_user_to_pool(self, ctx, channel):
        users = Users()
        if users.get_user_value(ctx.author.id,'datefake'):
            users.update_user_value(ctx.author.id,True,'datefake')
            users.update_user_value(ctx.author.id, datetime.now(timezone.utc), 'datefake_join_date')
            await ctx.author.add_roles(ctx.author.guild.get_role(self.role_id))
            await channel.send("Você foi adicionado na lista de participantes do evento.")
        else:
            users.insert_user_value(ctx.author.id,ctx.author.name,'name')
            users.update_user_value(ctx.author.id,ctx.author.nick,'nickname')
            try:
                users.update_user_value(ctx.author.id,True,'datefake')
                users.update_user_value(ctx.author.id, datetime.now(timezone.utc), 'datefake_join_date')
                await ctx.author.add_roles(ctx.author.guild.get_role(self.role_id))
                await channel.send("Você foi adicionado na lista de participantes do evento.")
            except Exception as e:
                await channel.send("Houve um erro ao adicionar você na lista :( tira print desta merda e manda pro Flakesu")
                await channel.send(f"Error: {e}")

    async def remove_user_from_pool(self, ctx, channel):
        users = Users()
        if users.get_user_value(ctx.author.id,'datefake'):
            users.update_user_value(ctx.author.id,False,'datefake')
            users.update_user_value(ctx.author.id, datetime.now(timezone.utc), 'datefake_leave_date')
            await ctx.author.remove_roles(ctx.author.guild.get_role(self.role_id))
            # ctx.author.remove_roles(ctx.get_role(self.role_id))
            await channel.send("Você foi removido da lista de participantes!")
        else:
            users.insert_user_value(ctx.author.id,ctx.author.name,'name')
            users.update_user_value(ctx.author.id,ctx.author.nick,'nickname')
            try:
                users.update_user_value(ctx.author.id,False,'datefake')
                users.update_user_value(ctx.author.id, datetime.now(timezone.utc), 'datefake_leave_date')
                await ctx.author.remove_roles(ctx.author.guild.get_role(self.role_id))
                # ctx.author.remove_roles(ctx.get_role(self.role_id))
                await channel.send("Você foi removido da lista de participantes!")
            except Exception as e:
                await channel.send("Houve um erro ao remover você da lista :( tira print desta merda e manda pro Flakesu")
                await channel.send(f"Error: {e}")
        

    async def check_participation(self, ctx):
        users = Users()
        tupla = users.get_user_value(ctx.author.id,'datefake')
        try:
            if tupla[0]:
                return True
            return False
        except TypeError:
            return False

    @commands.command(name='datefake',
        brief=f'Ex: $datefake',
        description='Cria um chat privado')
    async def _datefake(self, ctx):
        event_name = "Datefake"
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

        '''msg = await channel.send("Você gostaria de convidar ou ser convidado(a) por alguém para o evento?")
        confirmation = await self.confirmation_react(ctx, msg)
        if confirmation:
            await self.invite_pair(ctx, channel)
        else:
            return await self.delete_channel(ctx, channel)

        return await self.delete_channel(ctx, channel)'''

    @commands.command(name='participants',
        brief=f'Ex: $participants',
        description='Retorna uma lista de participantes')
    @commands.has_permissions(manage_guild=True)
    async def _participants(self, ctx):
        users = Users()
        users_list = [y for y in users.get_all_users_values('name','nickname','datefake') if y[-1]]
        output = f'Total de participantes: {len(users_list)}'
        for user in users_list:
            if user[1]:
                output += f"\n{user[1]}"
            else:
                output += f"\n{user[0]}"
        await ctx.send(output)

def setup(bot):
    bot.add_cog(Datefake(bot))