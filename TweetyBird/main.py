from discord.ext import commands, tasks

from dotenv import load_dotenv

from utils import constants, discord_utils, settings, twitter_utils

import os


# Discord Bot Setup

bot = commands.Bot(command_prefix='!',
                   case_insensitive=True,
                   description=constants.TweetyBirdDesc)


@bot.event
async def on_ready():
    """
    Triggers when bot starts.
    """
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def LoadCog(ctx, extension):
    bot.load_extension(f'Cogs.{extension}')


@bot.command()
async def UnLoadCog(ctx, extension):
    bot.unload_extension(f'Cogs.{extension}')


@bot.command()
async def ReLoadCog(ctx, extension):
    bot.unload_extension(f'Cogs.{extension}')
    bot.load_extension(f'Cogs.{extension}')


bot.load_extension("Cogs.mainCog")

twitter_utils.Verify_Twitter_Credentials()
bot.run(settings.Discord_Token)
