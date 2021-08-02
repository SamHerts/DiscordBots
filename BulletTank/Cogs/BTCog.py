from discord.ext import commands

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
