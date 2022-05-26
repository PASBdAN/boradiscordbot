from discord.ext import commands
from discord import Embed
from datetime import datetime, timezone
from database.client import Client
import random


class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.module_name = "Roulette"

    def create_embed(self, title:str, fields:list, image, colour, footer = ''):
        embed = Embed(title=title)
        fields = fields
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_image(url=image)
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
        print(f'Módulo {self.module_name} pronto!')


    # COMMANDS
    @commands.command(
        name='roll',
        brief=f'Ex: $roll',
        description='Retorna uma embed message interagível por reactions de um usuário do servidor')
    @commands.has_permissions(manage_guild=True)
    async def _roll(self, ctx):
        db = Client('Users')
        members_list = db.select('id')
        db.close_db()
        random.shuffle(members_list)
        member = ctx.guild.get_member(members_list[0][0])
        db = Client('MarryUsers')
        is_married = 'Reaja para se casar!'
        user_id = db.select('user_id',married_user = member.id)
        db.close_db()
        if user_id:
            is_married = f'Usuário já é casado com {ctx.guild.get_member(user_id[0][0]).display_name}'
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
            0xff66cc, is_married))
        if await self.confirmation_react(ctx,msg):
            db = Client('MarryUsers')
            db.insert(user_id = ctx.author.id, married_user = member.id, created_at = datetime.now(timezone.utc))
            db.close_db()
            await ctx.send(f'{ctx.author.display_name} e {member.display_name} são casados 💖')

def setup(bot):
    bot.add_cog(Roulette(bot))