from discord.ext import commands
from discord import Embed
from datetime import datetime, timezone
from database.client import Client
import random


class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.module_name = "Roulette"

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
        db = Client('Users')
        self.members_id_list = [x[0] for x in db.select('id')]
        db.close_db()
        print(f'Módulo {self.module_name} pronto!')


    # COMMANDS
    @commands.command(
        name='roll',
        brief=f'Ex: $roll',
        description='Retorna uma embed message interagível por reactions de um usuário do servidor')
    @commands.has_permissions(manage_guild=True)
    async def _roll(self, ctx):
        random.shuffle(self.members_id_list)
        member = ctx.guild.get_member(self.members_id_list[0])
        db = Client('MarryUsers')
        is_married = False
        user_id = db.select('user_id',married_user = member.id)
        married_message = 'Reaja para se casar!'
        db.close_db()
        if user_id:
            married_message = f'Usuário já é casado com {ctx.guild.get_member(user_id[0][0]).display_name}'
            is_married = True
        greater_role = member.roles[0]
        for role in member.roles[1:]:
            if role.position > greater_role.position:
                greater_role = role

        msg = await ctx.send(embed = self.create_embed(
            member.name,
            [
                ("Role: ",greater_role.name,False),
            ],
            member.avatar_url,
            0xff66cc, married_message))
        if is_married:
            return None
        if await self.confirmation_react(ctx,msg):
            db = Client('MarryUsers')
            db.insert(user_id = ctx.author.id, married_user = member.id, created_at = datetime.now(timezone.utc))
            db.close_db()
            await ctx.send(f'{ctx.author.display_name} e {member.display_name} são casados 💖')

    @commands.command(
        name='mymarry',
        brief=f'Ex: $mymarry',
        description='Retorna o seu harem!')
    @commands.has_permissions(manage_guild=True)
    async def _mymarry(self, ctx):
        db = Client('MarryUsers')
        marry_id_list = [x[0] for x in db.select('married_user',user_id = ctx.author.id)]
        db.close_db()
        casou = ''
        embed_lines = []
        for user_id in marry_id_list:
            casou += f'\n - {ctx.guild.get_member(user_id).display_name}'
        if not casou:
            casou = ' - Você não casou com ninguém ainda...'
        embed_lines.append(('Casou com:',casou,False))
        casado = ' - Ninguém se casou com você ainda...'
        db = Client('MarryUsers')
        married_to = [x[0] for x in db.select('user_id',married_user = ctx.author.id)]
        if married_to:
            casado = f' - {ctx.guild.get_member(married_to[0]).display_name}'
        embed_lines.append(('Está casado com:',casado,False))
        msg = await ctx.send(embed = self.create_embed(
            f'Harem do {ctx.author.display_name}',
            embed_lines,
            None,
            0xff66cc,
            '',
            ctx.author.avatar_url))

def setup(bot):
    bot.add_cog(Roulette(bot))