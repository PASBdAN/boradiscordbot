from discord.ext import commands
from discord import Embed
from datetime import datetime, timezone
from database.client import Client
import random


class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.module_name = "Roulette"
        db = Client('Users')
        self.members_dict = {x[0]:[x[1],x[2]] for x in db.select('id','roll_count','roll_timestamp')}
        db.close_db()
        self.roll_limit = 5
        self.roll_cooldown = 60

    def create_embed(self, title:str, fields:list, image, colour, footer = '', thumbnail = None):
        embed = Embed(title=title)
        fields = fields
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        if image:
            embed.set_image(url=image)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        embed.colour = colour
        embed.set_footer(text = footer)
        return embed

    async def block_roll(self, ctx):
        users = Client('Users')
        users.update_by_id(id=ctx.author.id,roll_count=self.roll_limit)
        users.close_db()
        return self.roll_limit

    async def unblock_roll(self, ctx):
        users = Client('Users')
        users.update_by_id(id=ctx.author.id,roll_count=0,roll_timestamp=datetime.now(timezone.utc))
        users.close_db()
        return self.roll_limit, datetime.now(timezone.utc)

    async def confirmation_react(self, ctx, msg, timeout = 20.0):
        accept =  "💖"
        await msg.add_reaction(accept)
        def check(reaction, user):
            return user == ctx.author and str(
                reaction.emoji) in [accept] and reaction.message == msg
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=timeout, check=check)
            if str(reaction.emoji) == accept:
                return True
        except Exception as e:
            return False

    # Inicialização do bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Módulo {self.module_name} pronto!')


    # COMMANDS
    @commands.command(
        name='roll',
        brief=f'Ex: b!roll',
        description='Retorna uma embed message interagível por reactions de um usuário do servidor')
    # @commands.has_permissions(manage_guild=True)
    @commands.has_role('Tester')
    async def _roll(self, ctx):
        author = self.members_dict[ctx.author.id]
        if author[0] > 4:
            diff = datetime.now(timezone.utc) - author[1]
            if int(diff.total_seconds() / 60) <= self.roll_cooldown:
                await self.block_roll(ctx)
                return await ctx.send(f'Você pode rolar novamente em {self.roll_cooldown - int(diff.total_seconds()/60)} minutos!')
            else:
                self.members_dict[ctx.author.id][0] = 0
                self.members_dict[ctx.author.id][1] = datetime.now(timezone.utc)
                await self.unblock_roll(ctx)
        self.members_dict[ctx.author.id][0] += 1

        members_id_list = list(self.members_dict.keys())
        random.shuffle(members_id_list)
        try:
            member = ctx.guild.get_member(members_id_list[0])
        except (TypeError, AttributeError):
            member = ctx.guild.fetch_member(members_id_list[0])
        
        db = Client('MarryUsers')
        user_id = db.select('user_id',married_user = member.id)
        db.close_db()

        married_message = 'Reaja para gadear!'
        is_married = False
        if user_id:
            married_message = f'Usuário já é dono(a) do gado(a) {ctx.guild.get_member(user_id[0][0]).display_name}'
            is_married = True

        greater_role = member.roles[0]
        for role in member.roles[1:]:
            if role.position > greater_role.position:
                greater_role = role

        msg = await ctx.send(embed = self.create_embed(
            member.name,
            [("Cargo: ",greater_role.name,False),],
            member.avatar_url,
            0xff66cc, married_message))
        if is_married:
            return None
        if await self.confirmation_react(ctx,msg):
            db = Client('MarryUsers')
            db.insert(user_id = ctx.author.id, married_user = member.id, created_at = datetime.now(timezone.utc))
            db.close_db()
            self.members_dict[ctx.author.id][0] = self.block_roll(ctx)

            await ctx.send(f'{ctx.author.display_name} é gado(a) de {member.display_name}!')

    @commands.command(
        name='mylist',
        brief=f'Ex: b!mylist',
        description='Retorna a sua listinha!')
    # @commands.has_permissions(manage_guild=True)
    @commands.has_role('Tester')
    async def _mylist(self, ctx):
        db = Client('MarryUsers')
        marry_id_list = [x[0] for x in db.select('married_user',user_id = ctx.author.id)]
        db.close_db()
        casou = ''
        embed_lines = []
        for user_id in marry_id_list:
            casou += f'\n - {ctx.guild.get_member(user_id).display_name}'
        if not casou:
            casou = ' - Você não é gado(a) de ninguém ainda...'
        embed_lines.append(('Gadeando:',casou,False))
        casado = ' - Ninguém está gadeando você ainda...'
        db = Client('MarryUsers')
        married_to = [x[0] for x in db.select('user_id',married_user = ctx.author.id)]
        if married_to:
            casado = f' - {ctx.guild.get_member(married_to[0]).display_name}'
        embed_lines.append(('É dono(a) do seguinte gado(a):',casado,False))
        msg = await ctx.send(embed = self.create_embed(
            f'Harem do {ctx.author.display_name}',
            embed_lines,
            None,
            0xff66cc,
            '',
            ctx.author.avatar_url))

def setup(bot):
    bot.add_cog(Roulette(bot))