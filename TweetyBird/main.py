from keep_alive import keep_alive
from replit import db
import discord
import os
from discord.ext import commands


client = discord.Client()
Discord_Token = os.environ['Discord_Token']
Twitter_API_PK = os.environ['Twitter_API_PK']
Twitter_API_SK = os.environ['Twitter_API_SK']

bot = commands.Bot(command_prefix='!')


def update_Following(TwitterUser):
    if "TwitterFollows" in db.keys():
        TwitterFollows = db["TwitterFollows"]
        if (TwitterUser in TwitterFollows):
            return "Twitter User already in Subscription List"
        else:
            TwitterFollows.append(TwitterUser)
            db["TwitterFollows"] = TwitterFollows
            return 'Adding' + TwitterUser + ' to Follow List'
    else:
        db["TwitterFollows"] = [TwitterUser]


def delete_Following(TwitterUser):
    TwitterFollows = db["TwitterFollows"]
    if TwitterUser in TwitterFollows:
        del TwitterFollows[TwitterFollows.index(TwitterUser)]
        db["TwitterFollows"] = TwitterFollows
        return "User was successfully removed!"
    else:
        return "User was not found in the subscription list."


def get_Following():
    if "TwitterFollows" in db.keys():
      TwitterFollows = db["TwitterFollows"]
      MyUsers = ""
      for User in TwitterFollows:
        MyUsers += User + ", "
      return MyUsers
    else:
        return "You do not currently follow any Twitter Users. Use '!FollowUser $AccountName' to subscribe to their tweets."


def Get_Help():
    return "TweetyBird Discord Bot - By SamH. Available commands:\n!Follow $Username ---Add a twitter account to the subscription list.\n!ListUsers -- List all currently subscribed twitter accounts.\n"



@bot.command()
async def test(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@bot.command()
async def Help(ctx):
  await ctx.send("Helping you!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('!Follow'):
        User = msg.split("!Follow", 1)[1]        
        await message.channel.send(update_Following(User))        

    if msg.startswith('!ListUsers'):        
      await message.channel.send(get_Following())

    if msg.startswith('!Unfollow'):
        removed = msg.split("!Unfollow", 1)[1]
        await message.channel.send(delete_Following(removed))    

keep_alive()
client.run(Discord_Token)
