from discord.ext import commands

from . import constants, settings, twitter_utils



#Discord Bot Setup
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


@bot.command(description=constants.FollowDescription)
async def follow(ctx, user: str):
    """
    Adds a new Twitter account to following list.
    """
    print('Got Follow Command')
    print(user)
    await ctx.send(twitter_utils.update_following(user))


@bot.command(description=constants.UnFollowDescription)
async def unfollow(ctx, user: str):
    """
    Removes a twitter account from the following list.
    """
    print('Got UnFollow Command')
    print(user)
    await ctx.send(twitter_utils.remove_user_from_following(user))


@bot.command(description=constants.ListUsersDescription)
async def list_users(ctx):
    """
    Lists users currently in the following list.
    """
    print('Got ListUsers Command')
    await ctx.send(twitter_utils.get_following())


@bot.command()
async def lookup(ctx, user: str):
    """
    Retrieves screen names of a twitter user.
    """
    print('Got Lookup Command')
    await ctx.send(twitter_utils.look_up_twitter_user(user))


@bot.command()
async def recent_tweet(ctx, user: str):
    """
    Gets the most recent tweet of a specified twitter account.
    """
    print('Got RecentTweet Command')
    await ctx.send(twitter_utils.get_recent_tweet_from_user(user))


@bot.command()
async def get_tweet(ctx):
    """
    Gets tweets from every user in following list.

    """
    following = db["TwitterFollows"]
    for user in following:
        await ctx.send(twitter_utils.get_most_recent_tweet_url(user))


bot.run(settings.Discord_Token)
