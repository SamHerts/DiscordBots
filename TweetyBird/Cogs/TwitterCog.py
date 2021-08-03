from utils.settings import Twitter_API_PK, Twitter_API_SK, Twitter_Access_Secret, Twitter_Access_Token
from discord.ext import commands

from utils import twitter_utils


GetAllDescription = "Retrieve most recent tweets from Subscription List"
FollowDescription = "Add a twitter account to the Subscription List"
UnFollowDescription = "Remove a twitter account from the Subscription List"
ListUsersDescription = "See what twitter accounts are being followed"
LookUpDescription = "Retrieve the screen name of a twitter account"
RecentTweetDescription = "Retrieve the most recent tweet from a twitter account"
StartStreamDescription = "Starts the stream of tweets"


class TwitIDConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        user = twitter_utils.getTwitUser(argument)
        if user is not None:
            return user
        raise commands.BadArgument(message="Not a valid Twitter User")


class TwitterCog(commands.Cog, name="Twitter"):
    def __init__(self, bot):
        self.bot = bot
        twitter_utils.Verify_Twitter_Credentials()
        #twitter_utils.start_stream(reload=False)

    @commands.command(description=FollowDescription)
    async def follow(self, ctx, user: TwitIDConverter):
        """
        Adds a new Twitter account to following list.
        """
        print('Got Follow Command')
        print(user)
        msg = twitter_utils.update_following(user)
        print(f"Message sent to discord: {msg}")
        await ctx.send(msg)
        #twitter_utils.start_stream(reload=True)
        #twitter_utils.start_stream(reload=False)

    @commands.command(description=UnFollowDescription)
    async def unfollow(self, ctx, user: TwitIDConverter):
        """
        Removes a twitter account from the following list.
        """
        print('Got UnFollow Command')
        print(user)
        await ctx.send(twitter_utils.remove_user_from_following(user))
        #twitter_utils.start_stream(reload=True)
        #twitter_utils.start_stream(reload=False)

    @commands.command(description=ListUsersDescription)
    async def list_users(self, ctx):
        """
        Lists users currently in the following list.
        """
        print('Got ListUsers Command')
        await ctx.send(twitter_utils.get_following())

    @commands.command(description=LookUpDescription)
    async def lookup(self, ctx, user: TwitIDConverter):
        """
        Retrieves screen names of a twitter user.
        """
        print('Got Lookup Command')
        await ctx.send(twitter_utils.look_up_twitter_user(user))

    @commands.command(description=RecentTweetDescription)
    async def recent_tweet(self, ctx, user: TwitIDConverter):
        """
        Gets the most recent tweet of a specified twitter account.
        """
        print('Got RecentTweet Command')
        twitter_utils.get_recent_tweet_from_user(user)

    @commands.command(description=StartStreamDescription)
    async def start_stream(self, ctx):
        print("Got LoadStream Command")
        twitter_utils.load_stream()


def setup(bot):
    bot.add_cog(TwitterCog(bot))


def teardown(bot):
    # twitter_utils.kill_stream()
    print('TwitterCog Successfully unloaded')
