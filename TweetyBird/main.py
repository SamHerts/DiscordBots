from discord.ext import commands, tasks

from dotenv import load_dotenv

from utils import constants, discord_utils, settings, twitter_utils



#Discord Bot Setup

bot = commands.Bot(command_prefix='!',
                   case_insensitive=True,
                   description=constants.TweetyBirdDesc)

@tasks.loop(seconds=60)
async def post_Tweets():
    print("Running Loop------\n")
    for user in twitter_utils.TwitterFollows:
        discord_utils.send_discord_message(twitter_utils.format_tweet(twitter_utils.get_recent_tweet_from_user(user)))


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
async def GetAll():
    print("Got GetAll Command")
    for user in twitter_utils.TwitterFollows:
        discord_utils.send_discord_message(twitter_utils.format_tweet(twitter_utils.get_recent_tweet_from_user(user)))

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
    await ctx.send(twitter_utils.format_tweet(twitter_utils.get_recent_tweet_from_user(user)))

twitter_utils.Verify_Twitter_Credentials()
bot.run(settings.Discord_Token)
