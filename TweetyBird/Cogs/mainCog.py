from discord.ext import commands


class mainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Administrator")
    async def LoadCog(self, ctx, extension):
        self.bot.load_extension(f'Cogs.{extension}')

    @commands.command()
    @commands.has_role("Administrator")
    async def UnLoadCog(self, ctx, extension):
        self.bot.unload_extension(f'Cogs.{extension}')

    @commands.command()
    @commands.has_role("Administrator")
    async def ReLoadCog(self, ctx, extension):
        self.bot.unload_extension(f'Cogs.{extension}')
        self.bot.load_extension(f'Cogs.{extension}')


def setup(bot):
    bot.add_cog(mainCog(bot))
