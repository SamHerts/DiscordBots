#from keep_alive import keep_alive
from replit import db
import discord
import os
from discord.ext import commands
import tweepy
import re


#Secret Keys
Discord_Token = os.environ['Discord_Token']
Twitter_API_PK = os.environ['Twitter_API_PK']
Twitter_API_SK = os.environ['Twitter_API_SK']
Twitter_Access_Token = os.environ['Twitter_Access_Token']
Twitter_Access_Secret = os.environ['Twitter_Access_Secret']
BotTestingWebhookURL = "https://discord.com/api/webhooks/859163753017901107/Qq78eRWL6YomGL249MVBOZgBXBdEHJ3p8wBkY0ojQLcBjWAm9tQtPJ2P3Z2UBFnjbZwD"

#Descriptions
TweetyBirdDesc = "TweetyBird Discord Bot - By SamH."
FollowDescription = "Add a twitter account to the subscription list"
UnFollowDescription = "Remove a twitter account from the subscription list"
ListUsersDescription = "See what twitter accounts are being followed"

#Regex Cached URL Finder
p = re.compile('(https://t.co/[a-zA-Z0-9]{10})')

webhook = discord.Webhook.from_url(BotTestingWebhookURL,adapter=RequestsWebhookAdapter())

########FUNCTION DEFINITIONS#############


#Add a username to the follow list
def update_Following(TwitterUser):
    if ValidUser(TwitterUser):
        TwitterUser_ID_STR = api.get_user(TwitterUser).id_str
        #Ensure database key exists
        if "TwitterFollows" in db.keys():
            TwitterFollows = db["TwitterFollows"]
            #Check for duplicates
            if (TwitterUser_ID_STR in TwitterFollows):
                return "Twitter User already in Subscription List"
            else:
                TwitterFollows.append(TwitterUser_ID_STR)
                db["TwitterFollows"] = TwitterFollows
                return 'Adding ' + TwitterUser + ' to Follow List'
        else:
            #Create new database key
            db["TwitterFollows"] = [TwitterUser_ID_STR]
            return 'Adding ' + TwitterUser + ' to Follow List'
    else:
        return "Not a valid Twitter Account"

#Check if user exists
def ValidUser(user):
    try:
        api.get_user(user).id
        return True
    except Exception:
        return False


#Remove a username from the follow list
def delete_Following(TwitterUser):
    TwitterFollows = db["TwitterFollows"]
    Twitteruser_ID = api.get_user(TwitterUser).id_str
    if Twitteruser_ID in TwitterFollows:
        del TwitterFollows[TwitterFollows.index(Twitteruser_ID)]
        db["TwitterFollows"] = TwitterFollows
        return "User was successfully removed!"
    else:
        return "User was not found in the subscription list."


#Print a list of followed users
def get_Following():
    emptyFollows = "You do not currently follow any Twitter Users. Use '!Follow $AccountName' to subscribe to their tweets."
    username_list = []
    if "TwitterFollows" in db.keys():
        TwitterFollows_ID = db["TwitterFollows"]
        if len(TwitterFollows_ID) == 0:
            return emptyFollows
        else:
            for userID in TwitterFollows_ID:
                username_list.append(api.get_user(userID).screen_name)
            return ", ".join(username_list)
    else:
        return emptyFollows

def LookUp(user):
    if ValidUser(user):
        return api.get_user(user).screen_name
    else:
        return "Twitter Account Does not Exist"

def GetRecentTweetURL(user):
    tweetURL = GetRecentTweet(user)
    if tweetURL == "Twitter Account Does not Exist":
      return tweetURL
    else:
      m = p.search(tweetURL)
      return m.group()
    

def GetRecentTweet(user):
    if ValidUser(user):
      return api.user_timeline(api.get_user(user).id, count=1)[0].text
    else:
      return "Twitter Account Does not Exist"


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
        webhook.send(status.text) 



myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(follow=["1342475881655259136"], is_async=True)


########DISCORD COMMAND DEFINITIONS#############

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
    print('Got ListUsers Command')
    await ctx.send(get_Following())


@bot.command()
async def lookup(ctx, user: str):
    print('Got Lookup Command')
    await ctx.send(LookUp(user))

@bot.command()
async def RecentTweet(ctx, user: str):
    print('Got RecentTweet Command')
    await ctx.send(GetRecentTweet(user))

@bot.command()
async def GetTweets(ctx):
  TwitterFollows = db["TwitterFollows"]
  for user in TwitterFollows:
    await ctx.send(GetRecentTweetURL(user))


########END DISCORD COMMAND DEFINITIONS#############



#keep_alive()
bot.run(Discord_Token)
