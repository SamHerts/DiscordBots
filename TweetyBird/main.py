#from keep_alive import keep_alive
from replit import db
import discord
import os
from discord.ext import commands
import tweepy



#Secret Keys
Discord_Token = os.environ['Discord_Token']
Twitter_API_PK = os.environ['Twitter_API_PK']
Twitter_API_SK = os.environ['Twitter_API_SK']
Twitter_Access_Token = os.environ['Twitter_Access_Token']
Twitter_Access_Secret = os.environ['Twitter_Access_Secret']

#Descriptions
TweetyBirdDesc = "TweetyBird Discord Bot - By SamH."
FollowDescription = "Add a twitter account to the subscription list"
UnFollowDescription = "Remove a twitter account from the subscription list"
ListUsersDescription = "See what twitter accounts are being followed"
########FUNCTION DEFINITIONS#############

#Add a username to the follow list
def update_Following(TwitterUser):
    if "TwitterFollows" in db.keys():
        TwitterFollows = db["TwitterFollows"]
        if (TwitterUser in TwitterFollows):
            return "Twitter User already in Subscription List"
        else:
            TwitterFollows.append(TwitterUser)
            db["TwitterFollows"] = TwitterFollows
            return 'Adding ' + TwitterUser + ' to Follow List'
    else:
        db["TwitterFollows"] = [TwitterUser]
        return 'Adding ' + TwitterUser + ' to Follow List'


#Remove a username from the follow list
def delete_Following(TwitterUser):
    TwitterFollows = db["TwitterFollows"]
    if TwitterUser in TwitterFollows:
        del TwitterFollows[TwitterFollows.index(TwitterUser)]
        db["TwitterFollows"] = TwitterFollows
        return "User was successfully removed!"
    else:
        return "User was not found in the subscription list."


#Print a list of followed users
def get_Following():
    emptyFollows = "You do not currently follow any Twitter Users. Use '!Follow $AccountName' to subscribe to their tweets."

    if "TwitterFollows" in db.keys():
        TwitterFollows = db["TwitterFollows"]
        if len(TwitterFollows) == 0:
            return emptyFollows
        else:
            return " ,".join(TwitterFollows)
    else:
        return emptyFollows


def Get_Follow_IDs(api):
    #Take in list of usernames -- return list of user IDs
    username_list = []
    if "TwitterFollows" in db.keys():
        TwitterFollows = db["TwitterFollows"]
        if len(TwitterFollows) == 0:
            return ""
        else:
            for username in TwitterFollows:
                username_list.append(api.get_user(username).id_str)
    else:
        return ""


########END FUNCTION DEFINITIONS#############

#Discord Bot Setup
bot = commands.Bot(command_prefix='!',
                   case_insensitive=True,
                   description=TweetyBirdDesc)

# Authenticate with Twitter
auth = tweepy.OAuthHandler(Twitter_API_PK, Twitter_API_SK)
auth.set_access_token(Twitter_Access_Token, Twitter_Access_Secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


#Tweepy Streaming tweets
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(follow=Get_Follow_IDs(), is_async=True)


#Discord Bot Ready and Commands
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(description=FollowDescription)
async def Follow(ctx, user: str):
    print('Got Follow Command')
    print(user)
    await ctx.send(update_Following(user))


@bot.command(description=UnFollowDescription)
async def UnFollow(ctx, user: str):
    print('Got UnFollow Command')
    print(user)
    await ctx.send(delete_Following(user))


@bot.command(description=ListUsersDescription)
async def ListUsers(ctx):
    print('Listing Subscription List')
    await ctx.send(get_Following())





#keep_alive()
bot.run(Discord_Token)
