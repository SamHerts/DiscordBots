
import discord
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

    @commands.Cog.listener()
    async def on_ready(self):
        print("BTCog has been loaded")

    @commands.command(description=JoinGameDescription)
    async def JoinGame(self, ctx):
        """
        Adds the author to the game
        """
        msg = None
        if BT.add_user(ctx.message.author.mention):
            msg = f'Adding you to the game, {ctx.message.author}'
        else:
            msg = f'Cannot add you to the game, either you are already in the game, there are too many players, or the game has already begun.'

        await ctx.send(msg)

    @commands.command(description=GetActionDescription, enabled=False)
    async def GetActionPoints(self, ctx):
        """
        Returns how many action points the author has
        """
        msg = "You do not have any action points"
        if BT.check_if_playing(ctx.message.author.mention):
            msg = BT.get_ac_points(ctx.message.author.mention)
        await ctx.send(msg)

    @commands.command(description=MoveDescription, enabled=False)
    async def Move(self, ctx, dir: str):
        """
        Moves a player if possible
        """
        msg = None
        if BT.check_if_playing(ctx.message.author.mention):
            if BT.move_player(ctx.message.author.mention, dir):
                msg = '**`SUCCESS`**'
            else:
                msg = "Unable to move you!"
        else:
            msg = "You're not playing right now!"

        await ctx.send(msg)

    @commands.command(description=ShootDescription, enabled=False)
    async def Shoot(self, ctx, target: discord.Member):
        """
        Shoots a target if possible
        """
        if BT.check_if_playing(ctx.message.author.mention):
            if BT.shoot_player(ctx.message.author.mention, target.mention):
                msg = "Nice shot! Your Range has been reset to 1"
            else:
                msg = "No shot, too bad"
        else:
            msg = "You're not even playing!"
        await ctx.send(msg)

    @commands.command(description=GiveActionDescription, enabled=False)
    async def GiveActionPoint(self, ctx, target: discord.Member):
        """
        Give an amount of action points to another player
        """
        if BT.check_if_playing(ctx.message.author.mention):
            if BT.send_ac_point(ctx.message.author.mention, target.mention):
                msg = "You've given one of your action points to someone else!"
            else:
                msg = "You can't give them an action point."
        else:
            msg = "You're not even playing!"
        await ctx.send(msg)

    @commands.command(enabled=False)
    async def IncreaseRange(self, ctx):
        """
        Increase the range of your tank -- up to a max of 3
        """
        if BT.check_if_playing(ctx.message.author.mention):
            if BT.increase_range(ctx.message.author.mention):
                msg = "You've increased your range!"
            else:
                msg = "Cannot increase range."
        else:
            msg = "You're not even playing!"
        await ctx.send(msg)

    @commands.command(description=RulesDescription)
    async def Rules(self, ctx):
        """
        Lists the rules of the game
        """
        await ctx.send(rules)

    @commands.command(description=ShowBoardDescription, enabled=False)
    async def ShowBoard(self, ctx):
        """
        Sends the current board state to Discord
        """
        async with ctx.typing():
            with BytesIO() as image_binary:
                BT.update_grid().save(image_binary, 'PNG')
                image_binary.seek(0)
                embed = discord.Embed(title=f'{self.bot.user.name} Map', description='\uFEFF',
                                      colour=ctx.author.colour, timestamp=ctx.message.created_at)
                image = discord.File(fp=image_binary, filename='Board.png')
                await ctx.send(embed=embed, file=image)

    @commands.command(name="RP", hidden=True)
    @commands.has_role("Administrator")
    async def release_points(self, ctx, amount: int):
        """
        Admin only: Give points to players
        """
        BT.admin_administer_points(amount)
        await ctx.send(f"Everyone has received {amount} action points!")

    @commands.command(hidden=True)
    @commands.has_role("Administrator")
    async def NewGame(self, ctx, grid_length, grid_height):
        """
        Admin only: start a new game
        """
        for command in self.get_commands():
            if command.name == "ShowBoard" or command.name == "IncreaseRange" or command.name == "GiveActionPoints" or command.name == "Shoot" or command.name == "Move" or command.name == "GetActionPoints" or command.name == "JoinGame"or command.name == "NewGame":
                command.enabled = not command.enabled
                print(f"Disabling {command.name}")

        async with ctx.typing():
            msg = str(BT.start_game(grid_length, grid_height))
            await ctx.send("A new game has begun! It is too late to join.\nGood Luck to all.")
            await ctx.send(msg)

    @NewGame.error
    async def NewGame_error(self, ctx, error):
        """A local Error Handler for the new game command.
        This will only listen for errors in NewGame.
        The global on_command_error will still be invoked after.
        """

        # Check if our required argument inp is missing.
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'grid_length' or error.param.name == 'grid_height':
                await ctx.send("You forgot to give me a grid size!\nTry NewGame 20 10")


def setup(bot):
    bot.add_cog(BTCog(bot))


def teardown(bot):
    print('BulletTank Cog Successfully Unloaded')


if __name__ == '__main__':
    print("This is a Discord Cog, no need to run this as main.")
