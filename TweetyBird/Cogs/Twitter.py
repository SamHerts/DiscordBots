from discord.ext import commands, tasks

from dotenv import load_dotenv

from utils import constants, discord_utils, settings, twitter_utils

import os


GetAllDescription = "Retrieve most recent tweets from Subscription List"
FollowDescription = "Add a twitter account to the Subscription List"
UnFollowDescription = "Remove a twitter account from the Subscription List"
ListUsersDescription = "See what twitter accounts are being followed"
LookUpDescription = "Retrieve the screen name of a twitter account"
RecentTweetDescription = "Retrieve the most recent tweet from a twutter account"


class Twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description=GetAllDescription)
    async def GetAll(self, ctx):
        print("Got GetAll Command")
        for user in twitter_utils.TwitterFollows:
            await ctx.send(twitter_utils.format_tweet(twitter_utils.get_recent_tweet_from_user(user)))

    @commands.command(description=FollowDescription)
    async def follow(self, ctx, user: str):
        """
        Adds a new Twitter account to following list.
        """
        print('Got Follow Command')
        print(user)
        msg = twitter_utils.update_following(user)
        print(f"Message sent to discord: {msg}")
        await ctx.send(msg)

    @commands.command(description=UnFollowDescription)
    async def unfollow(self, ctx, user: str):
        """
        Removes a twitter account from the following list.
        """
        print('Got UnFollow Command')
        print(user)
        await ctx.send(twitter_utils.remove_user_from_following(user))

    @commands.command(description=ListUsersDescription)
    async def list_users(self, ctx):
        """
        Lists users currently in the following list.
        """
        print('Got ListUsers Command')
        await ctx.send(twitter_utils.get_following())

    @commands.command(description=LookUpDescription)
    async def lookup(self, ctx, user: str):
        """
        Retrieves screen names of a twitter user.
        """
        print('Got Lookup Command')
        await ctx.send(twitter_utils.look_up_twitter_user(user))

    @commands.command(description=RecentTweetDescription)
    async def recent_tweet(self, ctx, user: str):
        """
        Gets the most recent tweet of a specified twitter account.
        """
        print('Got RecentTweet Command')
        await ctx.send(twitter_utils.format_tweet(twitter_utils.get_recent_tweet_from_user(user)))


def setup(bot):
    bot.add_cog(Twitter(bot))
