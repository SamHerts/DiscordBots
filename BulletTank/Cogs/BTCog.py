from discord.ext import commands
import Game.GameDriver
from dhooks import Embed, Webhook

JoinGameDescription = "Add your tank to the game!"
GetActionDescription = "How many action points do you currently have?"
MoveDescription = "Move your tank in a direction"
ShootDescription = "Rain fire on the enemy!"
GiveActionDescription = "Be a friend - give an action point to someone else"
RulesDescription = "List the rules of the game"


class BTCog(commands.Cog, name="Bullet Tank Game"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description=JoinGameDescription)
    async def JoinGame(self, ctx):
        """
        Adds the author to the game -- only if a game isn't currently in progress
        """
        if GameDriver.add_user(ctx.message.author):
            await ctx.send(f'Adding you to the game, {ctx.message.author}')

    @commands.command(description=GetActionDescription)
    async def GetActionPoints(self, ctx):
        """
        Returns how many action points the author has
        """

    @commands.command(description=MoveDescription)
    async def Move(self, ctx):
        """
        Moves a player if possible
        """

    @commands.command(description=ShootDescription)
    async def Shoot(self, ctx):
        """
        Shoots a target if possible
        """

    @commands.command(description=GiveActionDescription)
    async def GiveActionPoint(self, ctx):
        """
        Give an amount of action points to another player
        """

    @commands.command(description=RulesDescription)
    async def Rules(self, ctx):
        """
        Lists the rules of the game
        """


def setup(bot):
    bot.add_cog(BTCog(bot))


def teardown(bot):
    # twitter_utils.kill_stream()
    print('BulletTank Cog Successfully unloaded')


def send_embed_webhook(avatar: str, status, link_list, text: str):
    """
    Send tweet to Discord with Webhook
    """
    print(f"Tweet: {text}")
    hook = Webhook(Discord_Webhook)

    embed = Embed(
        description=text,
        color=0x1E0F3,
        timestamp="now",
    )
    if link_list is not None:
        if len(link_list) == 1:
            print(f"Found one image: {link_list[0]}")
            embed.set_image(link_list[0])

        elif len(link_list) > 1:
            print("Found more than one image")
            embed.set_image(link_list[0])

    embed.set_author(
        icon_url=avatar,
        name=status.user.screen_name,
        url=f"https://twitter.com/i/web/status/{status.id}",
    )

    hook.send(embed=embed)

    print("Webhook posted.")
