
from discord import File, Member
from discord.ext import commands
import Game.GameDriver as BT
from utils.BTsettings import BT_Discord_Webhook
from io import BytesIO

JoinGameDescription = "Add your tank to the game!"
GetActionDescription = "How many action points do you currently have?"
MoveDescription = "Move your tank in a direction"
ShootDescription = "Rain fire on the enemy!"
GiveActionDescription = "Be a friend - give an action point to someone else"
RulesDescription = "List the rules of the game"
ShowBoardDescription = "Displays the current board state"

rules = """
    Rules:

    Last Player standing wins.
    Each day, players receive at least 1 Action Point.
    Action points are lost upon use
    Action points can be transferred to other players
    Actions you can take:
    Move one space
    Shoot at a player within range
    Increase range - up to 3
    Transfer an Action Point to another Player
    Each Player starts with 4 hearts, if you run out of hearts you die.
    Defeated Players are added to the Angel Box and vote to give out bonus Action Points.
    A player must receive 30% of the vote to receive the Action Point
    """


class BTCog(commands.Cog, name="Bullet Tank Game"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description=JoinGameDescription)
    async def JoinGame(self, ctx):
        """
        Adds the author to the game -- only if a game isn't currently in progress
        """
        msg = None
        if BT.add_user(ctx.message.author):
            msg = f'Adding you to the game, {ctx.message.author}'
        else:
            msg = f'Cannot add you to the game, either you are already in the game, there are too many players, or the game has already begun.'

        await ctx.send(msg)

    @commands.command(description=GetActionDescription)
    async def GetActionPoints(self, ctx):
        """
        Returns how many action points the author has
        """
        msg = "You do not have any action points"
        if BT.check_if_playing(ctx.message.author):
            msg = BT.get_ac_points(ctx.message.author)
        await ctx.send(msg)

    @commands.command(description=MoveDescription)
    async def Move(self, ctx, dir: str):
        """
        Moves a player if possible
        """
        msg = None
        if BT.check_if_playing(ctx.message.author):
            if BT.move_player(ctx.message.author, dir):
                msg = '**`SUCCESS`**'
            else:
                msg = "Unable to move you!"
        else:
            msg = "You're not playing right now!"

        await ctx.send(msg)

    @commands.command(description=ShootDescription)
    async def Shoot(self, ctx, target: Member):
        """
        Shoots a target if possible
        """
        if BT.check_if_playing(ctx.message.author):
            if BT.shoot_player(ctx.message.author, target):
                msg = "Nice shot!"
            else:
                msg = "No shot, too bad"
        else:
            msg = "You're not even playing!"
        await ctx.send(msg)

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
        await ctx.send(rules)

    @commands.command(description=ShowBoardDescription)
    async def ShowBoard(self, ctx):
        """
        Sends the current board state to Discord
        """
        async with ctx.typing():
            with BytesIO() as image_binary:
                BT.update_grid().save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=File(fp=image_binary, filename='Board.png'))

    @commands.command(name="RP", hidden=True)
    @commands.has_role("Administrator")
    async def release_points(self, ctx):
        """
        Admin only: Give points to players
        """
        BT.admin_administer_points()
        await ctx.send("Everyone has received an action point!")


def setup(bot):
    bot.add_cog(BTCog(bot))
    print('BulletTank Cog Successfully Loaded')


def teardown(bot):
    # twitter_utils.kill_stream()
    print('BulletTank Cog Successfully Unloaded')


if __name__ == '__main__':
    print("This is a Discord Cog, no need to run this as main.")
