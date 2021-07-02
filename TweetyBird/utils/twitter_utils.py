import re

import tweepy

from .settings import Twitter_API_PK, Twitter_API_SK, Twitter_Access_Token, Twitter_Access_Secret
from .file_utils import open_json_file, save_json_file


# Persistent data
twitter_json_file = './data/twitter.json'
TwitterFollows = open_json_file('./data/twitter.json')

# Authenticate with Twitter
auth = tweepy.OAuthHandler(Twitter_API_PK, Twitter_API_SK)
auth.set_access_token(Twitter_Access_Token, Twitter_Access_Secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def is_valid_twitter_user(user):
    """
    Tries to retrieve a user using the Tweepy api. If it fails,
    then the user is not valid.
    """
    retrieved_user = None
    try:
        retrieved_user = api.get_user(user)
        print(f"Valid Twitter user: {retrieved_user.name}(@{retrieved_user.screen_name})")
    except Exception as err:
        print(f'Probably not a valid user: {err}')
    return retrieved_user is not None


def Verify_Twitter_Credentials():
    try:
        api.verify_credentials()
        print("Twitter API Authentication OK")
    except Exception:
        print("Error during Twitter API Authentication")


# Regex Cached Twitter URL Finder
p = re.compile('(https://t.co/[a-zA-Z0-9]{10})')


@save_json_file(filepath=twitter_json_file, contents=TwitterFollows)
def update_following(twitter_user):
    """
    If the provided user is a valid Twitter user:
      - Add the user to the following list      
    """
    msg = "Not a valid Twitter Account"
    if is_valid_twitter_user(twitter_user):
        twitter_user = api.get_user(twitter_user)
        if not TwitterFollows:
            msg = f"Adding {twitter_user.name}(@{twitter_user.screen_name}) to Follow List."
            TwitterFollows.update({twitter_user.id_str:twitter_user.name})
        elif twitter_user.id_str in TwitterFollows:
            msg = f"{twitter_user.name}(@{twitter_user.screen_name} is already in Subscription List." 
        else:
            msg = f"Adding {twitter_user.name}(@{twitter_user.screen_name}) to Follow List."
            TwitterFollows.update({twitter_user.id_str:twitter_user.name})
    print(msg)                    
    return msg


@save_json_file(filepath=twitter_json_file, contents=TwitterFollows)
def remove_user_from_following(twitter_user):
    """
    If a valid twitter user is provided:
      - Remove the user id from the following list if it's there
    """
    msg = "Twitter Account does not exist"
    if is_valid_twitter_user(twitter_user):
        twitter_user = api.get_user(twitter_user)
        if twitter_user.id_str in TwitterFollows:
            TwitterFollows.pop(twitter_user.id_str)
            msg = f"{twitter_user.name}(@{twitter_user.screen_name}) was removed from Subscription List."
        else:
            msg = f"You are not subscribed to{twitter_user.name}(@{twitter_user.screen_name})."   
    return msg


def get_following():
    """
    Gets the list of followers and returns a string list of their screen names.
    """    
    if not TwitterFollows:
        msg = "You do not currently follow any Twitter Users. Use '!Follow $AccountName' to subscribe to tweets."
    else:
        msg = ',\n'.join(TwitterFollows.values())               
    print(msg)
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


def get_recent_tweet_from_user(user):
    """
    Gets most recent tweet from a user.
    Validated means user is a status_object
    """
    msg = "Twitter Account does not exist"
    if isinstance(user, tweepy.User):
        msg = api.user_timeline(user.id, count=1)[0]
    elif isinstance(user,int):
        msg = api.user_timeline(api.get_user(user).id, count=1)[0] 
    elif isinstance(user, str) and is_valid_twitter_user(user):
        msg = api.user_timeline(api.get_user(user).id, count=1)[0]
    return msg


def get_most_recent_tweet_url(user):
    """
    Gets the most recent tweet url from a user.
    """
    tweet_url = get_recent_tweet_from_user(user)
    if tweet_url == "Twitter Account Does not Exist":
        return tweet_url
    else:
        # Regex to look for twitter URL
        m = p.search(tweet_url.text)
        return m.group()


def format_tweet(status):
    """
    Gets a tweet and formats it.
    """
    print(status.id)    
    print(status.user.name)
    print(status.text)
    return f"New Tweet from: {status.user.name}(@{status.user.screen_name})\n\n{status.text}"
