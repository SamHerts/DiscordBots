#from keep_alive import keep_alive
#For replit databases
from replit import db
#For WeBhooks
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
#For Secret Keys
import os
#For Discord Bot
from discord.ext import commands
#For Twitter API
import tweepy
#For Regex
import re


#Secret Keys
Discord_Token = os.environ['Discord_Token']
Twitter_API_PK = os.environ['Twitter_API_PK']
Twitter_API_SK = os.environ['Twitter_API_SK']
Twitter_Access_Token = os.environ['Twitter_Access_Token']
Twitter_Access_Secret = os.environ['Twitter_Access_Secret']
Discord_Webhook = os.environ['Discord_WebHook']

#Descriptions
TweetyBirdDesc = "TweetyBird Discord Bot - By SamH."
FollowDescription = "Add a twitter account to the subscription list"
UnFollowDescription = "Remove a twitter account from the subscription list"
ListUsersDescription = "See what twitter accounts are being followed"

#Regex Cached URL Finder
p = re.compile('(https://t.co/[a-zA-Z0-9]{10})')

########FUNCTION DEFINITIONS#############

#Modify the default Twitter Stream, and overwrite the default on_status call
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        SendMessage(PrepTweet(status)) 

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
  if ValidUser(TwitterUser):
    TwitterFollows = db["TwitterFollows"]
    Twitteruser_ID = api.get_user(TwitterUser).id_str
    if Twitteruser_ID in TwitterFollows:
        del TwitterFollows[TwitterFollows.index(Twitteruser_ID)]
        db["TwitterFollows"] = TwitterFollows
        return "User was successfully removed!"
    else:
        return "User was not found in the subscription list."
  else: 
    return "Twitter Account Does not Exist"


#Print a list of followed users
def get_Following():
    emptyFollows = "You do not currently follow any Twitter Users. Use '!Follow $AccountName' to subscribe to their tweets."
    username_list = []
    #Ensure db exists
    if "TwitterFollows" in db.keys():
        TwitterFollows_ID = db["TwitterFollows"]
        if len(TwitterFollows_ID) == 0:
            return emptyFollows
        else:
          #Convert twitter ID to username and return a list
            for userID in TwitterFollows_ID:
                username_list.append(api.get_user(userID).screen_name)
            return ", ".join(username_list)
    else:
        return emptyFollows

#Looks up the screen name of specified user/ID
def LookUp(user):
    if ValidUser(user):
        return api.get_user(user).screen_name
    else:
        return "Twitter Account Does not Exist"
#Get Recent Tweet wrapper for URL regex only
def GetRecentTweetURL(user):
    tweetURL = GetRecentTweet(user)
    if tweetURL == "Twitter Account Does not Exist":
      return tweetURL
    else:
      #Regex to look for twitter URL
      m = p.search(tweetURL)
      return m.group()
    
#Pulls the most recent tweet from specified user
def GetRecentTweet(user):
    if ValidUser(user):
      #this could get cleaned up
      return api.user_timeline(api.get_user(user).id, count=1)[0].text
    else:
      return "Twitter Account Does not Exist"

#Gets a status (Tweet) object and outputs it in a desired format
def PrepTweet(status):
    print(status.id)
    username = api.get_user(status.id)
    print(username)
    print(status.text)
    return "New Tweet from: {}\n\n{}".format(username,status.text)

#Discord Async WebHook Send message
async def SendMessage(message):
  async with aiohttp.ClientSession as session:
    webhook = Webhook.from_url(Discord_Webhook, adapter=AsyncWebhookAdapter(session))
    await webhook.send(message)


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

#Tweepy Stream setup
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
#Filter requires list of ID's and a filter level (none, low, medium, high)
myStream.filter(follow=db["TwitterFollows"], is_async=True, filter_level="medium")


########DISCORD COMMAND DEFINITIONS#############

#Discord Bot Ready and Commands

#When the bot is alive
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#Adds a new Twitter Account to follow
@bot.command(description=FollowDescription)
async def Follow(ctx, user: str):
    print('Got Follow Command')
    print(user)
    await ctx.send(update_Following(user))

#Removes a twitter account from follow list
@bot.command(description=UnFollowDescription)
async def UnFollow(ctx, user: str):
    print('Got UnFollow Command')
    print(user)
    await ctx.send(delete_Following(user))

#Lists users currently in follow list
@bot.command(description=ListUsersDescription)
async def ListUsers(ctx):
    print('Got ListUsers Command')
    await ctx.send(get_Following())

#Gets screen_name of twitter user
@bot.command()
async def lookup(ctx, user: str):
    print('Got Lookup Command')
    await ctx.send(LookUp(user))

#Gets the most recent tweet of a specified twitter account
@bot.command()
async def RecentTweet(ctx, user: str):
    print('Got RecentTweet Command')
    await ctx.send(GetRecentTweet(user))

#Gets tweets from every user in follow list
@bot.command()
async def GetTweets(ctx):
  TwitterFollows = db["TwitterFollows"]
  for user in TwitterFollows:
    await ctx.send(GetRecentTweetURL(user))


########END DISCORD COMMAND DEFINITIONS#############



#keep_alive()
bot.run(Discord_Token)
