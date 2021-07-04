from discord.ext import commands


from utils import settings, twitter_utils


# Discord Bot Setup
TweetyBirdDescription = "TweetyBird Discord Bot - By SamH."

bot = commands.Bot(command_prefix='!',
                   case_insensitive=True,
                   description=TweetyBirdDescription)


@bot.event
async def on_ready():
    """
    Triggers when bot starts.
    """
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

if __name__ == "__main__":
    bot.load_extension("Cogs.MainCog")
    bot.run(settings.Discord_Token)
