from discord.ext import commands
from discord import Embed
from vrchat.bot import Bot
import asyncio

class VrChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vrchat_bot = Bot()
        self.vrchat_bot.open_api()

    def create_embed(self, title:str, fields:list, image, colour, footer = ''):
        embed = Embed(title=title)
        fields = fields
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_image(url=image)
        embed.colour = colour
        embed.set_footer(text = footer)
        return embed
    
    # EVENT LISTENERS
    @commands.Cog.listener()
    async def on_ready(self):
        print('Módulo de VRChat pronto!')

    # TASKS
    

    # COMMANDS

    @commands.command(
        brief=f'Ex: $search_worlds "Bar do Zé"',
        description='Retorna uma embed message interagível por reactions dos mundos retornados na pesquisa')
    @commands.has_permissions(manage_guild=True)
    async def search_worlds(self, ctx, *args):
        world_name = ' '.join(args)
        worlds = self.vrchat_bot.get_worlds(world_name)
        i = 0
        msg = await ctx.send(embed = self.create_embed(worlds[i].name,[
            ("Autor",worlds[i].author_name,True),
            ("Capacidade",worlds[i].capacity,True),
            ("Favoritos",worlds[i].favorites,True),
            ("World ID",worlds[i].id,False)],
            worlds[i].image_url,
            0xff66cc,f"{i+1}/{len(worlds)}"))
        left = "⬅️"
        right = "➡️"
        # join =  "☑️"
        await msg.add_reaction(left)
        await msg.add_reaction(right)
        def check(reaction, user):
            return user == ctx.author and str(
                reaction.emoji) in [left, right] and reaction.message == msg
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=10.0, check=check)
                if str(reaction.emoji) == left:
                    if i == 0:
                        i = len(worlds) - 1
                    else:
                        i -= 1
                    await msg.edit(embed=self.create_embed(worlds[i].name,[
                        ("Autor",worlds[i].author_name,True),
                        ("Capacidade",worlds[i].capacity,True),
                        ("Favoritos",worlds[i].favorites,True),
                        ("World ID",worlds[i].id,False)],
                        worlds[i].image_url,
                        0xff66cc,f"{i+1}/{len(worlds)}"))
                if str(reaction.emoji) == right:
                    if i == len(worlds) - 1:
                        i = 0
                    else:
                        i += 1
                    await msg.edit(embed=self.create_embed(worlds[i].name,[
                        ("Autor",worlds[i].author_name,True),
                        ("Capacidade",worlds[i].capacity,True),
                        ("Favoritos",worlds[i].favorites,True),
                        ("World ID",worlds[i].id,False)],
                        worlds[i].image_url,
                        0xff66cc,f"{i+1}/{len(worlds)}"))
            except asyncio.TimeoutError:
                break


    '''@commands.command(
        brief=f'Ex: $send_friend_request Flakesu Ciri♥ Tarado',
        description="Envie um friend request do bot para os usuários especificados")
    @commands.has_permissions(manage_guild=True)
    async def send_friend_request(self, ctx, *args):
        for user in args:
            usuario = self.vrchat_bot.send_friend_request(user)
            if usuario:
                await ctx.send(f"Pedido de amizade enviado ao usuário {usuario.display_name}!")
            else:
                await ctx.send(f"Houve um erro no ao enviar friend request ao usuário {user}")'''


    '''@commands.command(
        brief=f'Ex: $invite_users <worldId> 69024 Friends+ Flakesu Ciri♥ Tarado',
        description="Cria uma instância do mundo com o worldId especificado. O primeiro argumento é o worldId do mundo que você quer criar a instância, sugiro conseguir ele com o comando $search_world. O segundo argumento é o modo da sala (public, friends, invite+, etc). O terceiro argumento é o id da instância do mundo. Os argumentos seguintes são nomes de usuários do VRChat.")
    @commands.has_permissions(manage_guild=True)
    async def invite_users(self, ctx, *args):
        for user in args[3:]:
            usuario = self.vrchat_bot.invite_user(
                args[0],
                args[1],
                args[2].lower(),
                "us",
                user)
            if usuario:
                await ctx.send(f"O usuário {usuario} foi convidado!")
            else:
                await ctx.send(f"Houve um erro ao convidar o usuário {user}")'''

def setup(bot):
    bot.add_cog(VrChat(bot))