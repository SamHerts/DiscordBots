
from typing import List
import discord
from discord.ext import commands
from Game import GameDriver as BT
from Game.Display import colors
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
    Action points can be transferred to other players for free
    Actions you can take:
    Move one space - N, S, E, W, NE. NW, SE, SW
    Shoot at a player within range
    Increase range - up to 3
    Transfer an Action Point to another Player
    Each Player starts with 4 hearts, if you run out of hearts you die.
    Defeated Players are added to the Angel Box and vote to give out bonus Action Points.
    A player must receive 30% of the vote to receive the Action Point
    """

toggle_commands = ["ShowBoard", "IncreaseRange", "GiveActionPoint", "Shoot",
                   "Move",  "GetActionPoints", "JoinGame", "NewGame", "WhereTheFuckAmI"]


class bullettank(commands.Cog, name="Bullet Tank Game"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("BTCog has been loaded")

    def bullet_tank_check():
        async def predicate(ctx):
            return ctx.author.has_role("playing bullet tank") or ctx.author.has_role("Testing")
        return commands.check(predicate)

    @commands.command(description=JoinGameDescription, aliases=['Join'])
    @commands.has_any_role("Testing", "playing bullet tank")
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

    @commands.command(description=GetActionDescription, enabled=False, aliases=['ActionPoints', 'AP'])
    @commands.has_any_role("Testing", "playing bullet tank")
    async def GetActionPoints(self, ctx):
        """
        Returns how many action points the author has
        """
        msg = "You do not have any action points"
        if BT.check_if_playing(ctx.message.author.mention):
            msg = BT.get_ac_points(ctx.message.author.mention)
        await ctx.send(msg)

    @commands.command(description=MoveDescription, enabled=False)
    @commands.has_any_role("Testing", "playing bullet tank")
    async def Move(self, ctx, dir: str):
        """
        Moves a player if possible
        """
        msg = None
        if BT.check_if_playing(ctx.message.author.mention):
            if BT.move_player(ctx.message.author.mention, dir):
                if dir == "N":
                    await ctx.message.add_reaction("⬆️")
                if dir == "E":
                    await ctx.message.add_reaction("➡️")
                if dir == "W":
                    await ctx.message.add_reaction("⬅️")
                if dir == "S":
                    await ctx.message.add_reaction("⬇️")
                if dir == "NE":
                    await ctx.message.add_reaction("↗️")
                if dir == "NW":
                    await ctx.message.add_reaction("↖️")
                if dir == "SE":
                    await ctx.message.add_reaction("↘️")
                if dir == "SW":
                    await ctx.message.add_reaction("↙️")
                msg = '**`SUCCESS`**'
            else:
                msg = "Unable to move you!"
        else:
            msg = "You're not playing right now!"

        await ctx.send(msg)

    @commands.command(description=ShootDescription, enabled=False)
    @commands.has_any_role("Testing", "playing bullet tank")
    async def Shoot(self, ctx, target: discord.Member):
        """
        Shoots a target if possible
        """
        if BT.check_if_playing(ctx.message.author.mention) and BT.check_if_playing(target.mention):
            if BT.shoot_player(ctx.message.author.mention, target.mention):
                msg = "Nice shot! Your Range has been reset to 1"
                await ctx.message.add_reaction("🔫")
            else:
                msg = "No shot, too bad"
                await ctx.message.add_reaction("❌")
        else:
            msg = "You or your target are not even playing!"
        await ctx.send(msg)

    @Shoot.error
    async def Shoot_error(self, ctx, error):
        """
        A local Error Handler for the Shoot game command.
        This will only listen for errors in Shoot.
        The global on_command_error will still be invoked after.
        """
        # Check if our required argument inp is missing.
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Who you trying to shoot? Try Shoot @Player")
        raise error

    @commands.command(description=GiveActionDescription, enabled=False, aliases=['Give'])
    @commands.has_any_role("Testing", "playing bullet tank")
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
    @commands.has_any_role("Testing", "playing bullet tank")
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
        # await ctx.message.add_reaction("🔫")
        await ctx.send(rules)

    @commands.command(enabled=False, aliases=['Where', 'Who', 'TheFuck?'])
    @commands.has_any_role("Testing", "playing bullet tank")
    async def WhereTheFuckAmI(self, ctx):
        """
        Tells you where the fuck you are
        """
        auth = ctx.message.author.mention
        if BT.check_if_playing(auth):
            color_hash = colors[BT.get_user_color(auth)]
            color_hex = "0X" + color_hash[1:]
            async with ctx.typing():

                embed = discord.Embed(
                    title=f"You're right the fuck there, at coordinates: {BT.where_the_fuck_am_i(auth)}",
                    color=int(color_hex, 0),
                    timestamp=ctx.message.created_at
                )
                embed.set_author(name=ctx.message.author,
                                 icon_url=ctx.message.author.avatar_url)

                await ctx.send(embed=embed)
        else:
            msg = "You're not even playing!"
            await ctx.send(msg)

    @commands.command(description=ShowBoardDescription, enabled=False, aliases=['ShowMap', 'Map', 'Board', 'Show'])
    @commands.has_any_role("Testing", "playing bullet tank")
    async def ShowBoard(self, ctx):
        """
        Sends the current board state to Discord
        """
        async with ctx.typing():
            with BytesIO() as image_binary:
                BT.update_grid().save(image_binary, 'PNG')
                image_binary.seek(0)
                embed = discord.Embed(title=f'{self.bot.user.name} Map', description=f"Players left alive: {BT.get_alive()}",
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

    @commands.command(name="AddPlayer", hidden=True)
    @commands.has_role("Administrator")
    async def add_player(self, ctx, player: discord.Member, Color: str, CoordsX, CoordsY, Health: int, Actions: int):
        """
        Admin only: Give points to players
        """
        print(
            f"{type(player)=}{player=}\n{type(Color)=}{Color=}\n{type(CoordsX)=}{CoordsX=}\n{type(Health)=}{Health=}")
        Coords = [int(CoordsX), int(CoordsY)]
        if BT.add_user(player.mention, debug=True, color=Color, coords=Coords, health=Health, actions=Actions):
            await ctx.send(f'Adding you to the game, {player.mention}')
        else:
            ctx.send(f'Cannot add player')

    @commands.command(hidden=True)
    @commands.has_role("Administrator")
    async def NewGame(self, ctx, grid_length: int, grid_height: int):
        """
        Admin only: start a new game
        """
        for command in self.get_commands():
            if command.name in toggle_commands:
                command.enabled = not command.enabled
                if command.enabled:
                    print(f"Enabling {command.name}")
                else:
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
        raise error

    # async def cog_command_error(self, ctx, error):
    #    if hasattr(ctx.command, 'on_error'):
    #        return
    #    if isinstance(error, )
    #    return await super().cog_command_error(ctx, error)


def setup(bot):
    bot.add_cog(bullettank(bot))


def teardown(bot):
    print('BulletTank Cog Successfully Unloaded')


if __name__ == '__main__':
    print("This is a Discord Cog, no need to run this as main.")
