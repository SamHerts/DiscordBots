import re

import tweepy

from .discord_utils import send_discord_message
from .settings import Twitter_API_PK, Twitter_API_SK, Twitter_Access_Token, Twitter_Access_Secret

TwitterFollows = {}

# Modify the default Twitter Stream, and overwrite the default on_status call
class TwitterStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        send_discord_message(format_tweet(status))


# Authenticate with Twitter
auth = tweepy.OAuthHandler(Twitter_API_PK, Twitter_API_SK)
auth.set_access_token(Twitter_Access_Token, Twitter_Access_Secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
try:
    api.verify_credentials()
    print("Authentication OK")
except Exception:
    print("Error during authentication")

# Tweepy Stream setup
myStreamListener = TwitterStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# Filter requires list of ID's and a filter level (none, low, medium, high)
myStream.filter(follow=TwitterFollows, is_async=True, filter_level="medium")

#Regex Cached Twitter URL Finder
p = re.compile('(https://t.co/[a-zA-Z0-9]{10})')


def update_following(twitter_user):
    """
    If the provided user is a valid Twitter user:
      - Add the user to the following list      
    """
    msg = "Not a valid Twitter Account"
    if is_valid_twitter_user(twitter_user):
        twitter_user = api.get_user(twitter_user)
        if twitter_user.id in TwitterFollows:
            msg = "Twitter User already in Subscription List"
        else:
            msg = 'Adding {} to Follow List'.format(twitter_user.name)
            TwitterFollows.update({twitter_user.id,twitter_user.name})       
    return msg


def is_valid_twitter_user(user):
    """
    Tries to retrieve a user using the Tweepy api. If it fails,
    then the user is not valid.
    """
    retrieved_user = None
    try:
        retrieved_user = api.get_user(user)
    except Exception as err:
        print(f'Probably not a valid user: {err}')
    return retrieved_user is not None


def remove_user_from_following(twitter_user):
    """
    If a valid twitter user is provided:
      - Remove the user id from the following list if it's there
    """
    msg = "Twitter Account does not exist"
    if is_valid_twitter_user(twitter_user):
        twitter_user = api.get_user(twitter_user)
        if twitter_user.id in TwitterFollows:
            TwitterFollows.pop(twitter_user.id)
            msg = "{} was removed from the Subscription List".format(twitter_user.name)
        else:
            msg = 'You were not Subscribed to {}\'s  tweets.'.format(twitter_user.name)      
    return msg


def get_following():
    """
    Gets the list of followers and returns a string list of their screen names.
    """    
    if not TwitterFollows:
        msg = "You do not currently follow any Twitter Users. Use '!Follow $AccountName' to subscribe to tweets."
    else:
        for user in TwitterFollows:
            msg = ', '.join(user.name)   
    return msg


def look_up_twitter_user(user):
    """
    If a valid twitter user is provided:
      - Return the user's screen name
    """
    msg = "Twitter account does not exist"
    if is_valid_twitter_user(user):
        msg = api.get_user(user).screen_name
    return msg


def get_recent_tweet_from_user(user,validated):
    """
    Gets most recent tweet from a user.
    """
    msg = "Twitter Account does not exist"
    if validated:
        msg = api.user_timeline(user.id, count=1)[0].text
    else:
        if is_valid_twitter_user(user):                  
            msg = api.user_timeline(api.get_user(user).id, count=1)[0].text
    return msg


def get_most_recent_tweet_url(user, validated):
    """
    Gets the most recent tweet url from a user.
    """
    tweet_url = get_recent_tweet_from_user(user,validated)
    if tweet_url == "Twitter Account Does not Exist":
        return tweet_url
    else:
        # Regex to look for twitter URL
        m = p.search(tweet_url)
        return m.group()


def format_tweet(status):
    """
    Gets a tweet and formats it.
    """
    print(status.id)    
    print(status.user.name)
    print(status.text)
    return f"New Tweet from: {status.user.name}\n\n{status.text}"
