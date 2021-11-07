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
    async def search_world(self, ctx, world_name):
        output = ""
        for world in self.vrchat_bot.get_worlds(world_name):
            output += f"\nNOME: {world.name}\n ID: {world.id}\n"
        await ctx.send(output)

    @commands.command(
        brief=f'Ex: $send_friend_request Flakesu Ciri♥ Tarado',
        description="Envie um friend request do bot para os usuários especificados")
    async def send_friend_request(self, ctx, *args):
        for user in args:
            usuario = self.vrchat_bot.send_friend_request(user)
            if usuario:
                await ctx.send(f"Pedido de amizade enviado ao usuário {usuario.display_name}!")
            else:
                await ctx.send(f"Houve um erro no ao enviar friend request ao usuário {user}")

    @commands.command(
        brief=f'Ex: $invite_users Friends+ 69024 Flakesu Ciri♥ Tarado',
        description="Cria uma instância do 1's Optimized Box")
    async def optimized_box(self, ctx, *args):
        for user in args[2:]:
            usuario = self.vrchat_bot.invite_user(
                "wrld_1a8b8684-3b19-4770-a4a7-288762f57b29",
                args[1],
                args[0].lower(),
                "us",
                user)
            if usuario:
                await ctx.send(f"O usuário {usuario} foi convidado!")
            else:
                await ctx.send(f"Houve um erro ao convidar o usuário {user}")
    
    @commands.command(
        brief=f'Ex: $invite_users Public 37452 Flakesu Ciri♥ Tarado',
        description="Cria uma instância do Bar do Zé Brasil 3 OFFICIAL")
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
        

def setup(bot):
    bot.add_cog(VrChat(bot))