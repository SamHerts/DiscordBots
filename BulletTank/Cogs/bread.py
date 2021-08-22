#import discord
from discord.ext import commands


class bread(commands.Cog, name="bread"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def greet(self, message):
        substr = str(message.content).lower()
        if substr.find("bread") != -1 or substr.find("toast") != -1:
            await message.add_reaction("🍞")

        await self.client.process_commands(message)


def setup(bot):
    bot.add_cog(bread(bot))


def teardown(bot):
    print('BulletTank Cog Successfully Unloaded')


if __name__ == '__main__':
    print("This is a Discord Cog, no need to run this as main.")
