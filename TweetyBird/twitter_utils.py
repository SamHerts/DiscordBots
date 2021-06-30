import re

from replit import db
import tweepy

from .discord_utils import send_discord_message
from .settings import Twitter_API_PK, Twitter_API_SK, Twitter_Access_Token, Twitter_Access_Secret


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
myStream.filter(follow=db["TwitterFollows"], is_async=True, filter_level="medium")

#Regex Cached URL Finder
p = re.compile('(https://t.co/[a-zA-Z0-9]{10})')


def update_following(twitter_user):
    """
    If the provided user is a valid Twitter user:
      - Add the user to the following
      - Init db if this is the first user
    """
    msg = "Not a valid Twitter Account"
    if is_valid_twitter_user(twitter_user):
        twitter_user_id_string = api.get_user(twitter_user).id_str
        # Ensure database key exists
        if "TwitterFollows" in db.keys():
            following = db["TwitterFollows"]
            # Check for duplicates
            if twitter_user_id_string in following:
                msg = "Twitter User already in Subscription List"
            else:
                following.append(twitter_user_id_string)
                db["TwitterFollows"] = following
                msg = 'Adding ' + twitter_user + ' to Follow List'
        else:
            # Create new database key
            db["TwitterFollows"] = [twitter_user_id_string]
            msg = 'Adding ' + twitter_user + ' to Follow List'
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
        following = db["TwitterFollows"]
        twitter_user_id = api.get_user(twitter_user).id_str
        if twitter_user_id in following:
            del following[following.index(twitter_user_id)]
            db["TwitterFollows"] = following
            msg = "User was successfully removed!"
        else:
            msg = "User was not found in the subscription list."
    return msg


def get_following():
    """
    Gets the list of followers and returns a string list of their screen names.
    """
    msg = "You do not currently follow any Twitter Users. Use '!Follow $AccountName' to subscribe to their tweets."
    # Ensure db exists
    if "TwitterFollows" in db.keys():
        following = db["TwitterFollows"]
        if len(following) > 0:
            # Convert twitter ID to username and return a list
            msg = ', '.join([api.get_user(uid).screen_name for uid in following])
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
    """
    msg = "Twitter account does not exist"
    if is_valid_twitter_user(user):
        # this could get cleaned up
        uid = api.get_user(user).id
        msg = api.user_timeline(uid, count=1)[0].text
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
        m = p.search(tweet_url)
        return m.group()


def format_tweet(status):
    """
    Gets a tweet and formats it.
    """
    print(status.id)
    username = api.get_user(status.id)
    print(username)
    print(status.text)
    return f"New Tweet from: {username}\n\n{status.text}"
