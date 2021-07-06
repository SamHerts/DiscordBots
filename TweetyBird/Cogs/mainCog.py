from discord.ext import commands


class MainCog(commands.Cog, name="General"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def LoadCog(self, ctx, *, cog: str):
        """
        Command which Loads a Module.
        """
        try:
            self.bot.load_extension(f'Cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def UnloadCog(self, ctx, *, cog: str):
        """
        Command which Unloads a Module.
        """
        try:
            self.bot.unload_extension(f'Cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.has_role("Administrator")
    async def ReloadCog(self, ctx, *, cog: str):
        """
        Command which Reloads a Module.
        """
        try:
            self.bot.unload_extension(f'Cogs.{cog}')
            self.bot.load_extension(f'Cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


def setup(bot):
    bot.add_cog(MainCog(bot))
