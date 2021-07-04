from discord.ext import commands


class ping(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def Ping(self, ctx):
        await ctx.send('Pong!')


def setup(bot):
    bot.add_cog(ping(bot))
