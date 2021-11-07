import discord
from discord.ext import commands
from vrchat.bot import Bot

class VrChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vrchat_bot = Bot()
        self.vrchat_bot.open_api()

    # EVENT LISTENERS
    @commands.Cog.listener()
    async def on_ready(self):
        print('Módulo de VRChat pronto!')

    # TASKS
    
    # COMMANDS
    @commands.command(
        brief=f'Ex: $search_world "Bar do Zé"',
        description='Lista os mundos e seus IDs dado um nome de pesquisa')
    @commands.has_any_role("Chefes do Role","Mestre do Role","Tester","PseudoPiranha","Piranha")
    async def search_world(self, ctx, world_name):
        output = ""
        for world in self.vrchat_bot.get_worlds(world_name):
            output += f"\nNOME: {world.name}\n ID: {world.id}\n"
        await ctx.send(output)

    @commands.command(
        brief=f'Ex: $send_friend_request Flakesu Ciri♥ Tarado',
        description="Envie um friend request do bot para os usuários especificados")
    @commands.has_any_role("Chefes do Role","Mestre do Role","Tester","PseudoPiranha","Piranha")
    async def send_friend_request(self, ctx, *args):
        for user in args:
            usuario = self.vrchat_bot.send_friend_request(user)
            if usuario:
                await ctx.send(f"Pedido de amizade enviado ao usuário {usuario.display_name}!")
            else:
                await ctx.send(f"Houve um erro no ao enviar friend request ao usuário {user}")

    @commands.command(
        brief=f'Ex: $invite_users wrld_e5c30b56-efa8-42d5-a8d4-a2cca2bf3403 Friends+ 69024 Flakesu Ciri♥ Tarado',
        description="Cria uma instância do mundo com o worldId especificado")
    @commands.has_any_role("Chefes do Role","Mestre do Role","Tester","PseudoPiranha","Piranha")
    async def invite_users(self, ctx, *args):
        for user in args[2:]:
            usuario = self.vrchat_bot.invite_user(
                args[0],
                args[2],
                args[1].lower(),
                "us",
                user)
            if usuario:
                await ctx.send(f"O usuário {usuario} foi convidado!")
            else:
                await ctx.send(f"Houve um erro ao convidar o usuário {user}")
    '''
    @commands.command(
        brief=f'Ex: $invite_users Public 37452 Flakesu Ciri♥ Tarado',
        description="Cria uma instância do Bar do Zé Brasil 3 OFFICIAL")
    @commands.has_any_role("Chefes do Role","Mestre do Role","Tester","PseudoPiranha","Piranha")
    async def bar_do_ze_3(self, ctx, *args):
        for user in args[2:]:
            usuario = self.vrchat_bot.invite_user(
                "wrld_3036938d-689f-47f8-a224-ab67b5059723",
                args[1],
                args[0].lower(),
                "us",
                user)
            if usuario:
                await ctx.send(f"O usuário {usuario} foi convidado!")
            else:
                await ctx.send(f"Houve um erro ao convidar o usuário {user}")
    '''        

def setup(bot):
    bot.add_cog(VrChat(bot))