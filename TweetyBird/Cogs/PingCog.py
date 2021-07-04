import discord

from discord.ext import commands


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            color=discord.Color.green(),
            timestamp=ctx.message.created_at
        )
        embed.set_author(name='Pong', icon_url=self.bot.user.avatar_url)
        embed.add_field(name=f'{round(self.bot.latency * 1000)}ms',
                        value='--------')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(PingCog(bot))
