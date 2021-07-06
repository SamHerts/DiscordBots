from re import sub, MULTILINE
from dhooks import Embed, Webhook
from tweepy import OAuthHandler, API, Status, Stream, User, StreamListener
from html import unescape


from .settings import Twitter_API_PK, Twitter_API_SK, Twitter_Access_Token, Twitter_Access_Secret, Discord_Webhook
from .file_utils import open_json_file, save_json_file


# Persistent data
twitter_json_file = './data/twitter.json'
TwitterFollows = open_json_file('./data/twitter.json')

# Regex Cached Twitter URL Finder
# p = re.compile('(https://t.co/[a-zA-Z0-9]{10})')


# Twitter Authentication
auth = OAuthHandler(Twitter_API_PK, Twitter_API_SK)
auth.set_access_token(Twitter_Access_Token, Twitter_Access_Secret)
api = API(auth)


class MyStreamListener(StreamListener):
    """
    Overwrites Tweepy's base streamlistener to send webhooks to discord
    """

    def on_status(self, status):
        """Called when a new status arrives"""
        print(f"on_status: {status.text}")
        # Tweet is retweet
        if hasattr(status, "retweeted_status"):
            print("Tweet is retweet")
            format_tweet(status=status)
            return

        # Tweet is a reply
        elif status.in_reply_to_user_id is not None:
            print("Tweet is a reply")
            format_tweet(status=status)
            return
        else:
            format(status=status)
            return

    def on_error(self, status_code):
        """Called when an error arrives"""
        print("Encountered streaming error (", status_code, ")")


def getTwitUser(user: str) -> User:
    """
    Checks Twitter API for Valid Twitter Account
    """
    retrieved_user = None
    try:
        retrieved_user = api.get_user(user)
        print(
            f"Valid Twitter user: {retrieved_user.name}(@{retrieved_user.screen_name})")
    except Exception as err:
        print(f'Probably not a valid user: {err}')
    return retrieved_user


def Verify_Twitter_Credentials():
    """
    Verify Twitter API Access is eligible
    """
    try:
        api.verify_credentials()
        print("Twitter API Authentication OK")
    except Exception:
        print("Error during Twitter API Authentication")


@save_json_file(filepath=twitter_json_file, contents=TwitterFollows)
def update_following(twitter_user: User) -> str:
    """
    Add the user to the Subscription list
    """
    if twitter_user.id_str in TwitterFollows:
        msg = f"{twitter_user.name}(@{twitter_user.screen_name} is already in Subscription List."
    else:
        msg = f"Adding {twitter_user.name}(@{twitter_user.screen_name}) to Follow List."
        TwitterFollows.update({twitter_user.id_str: twitter_user.name})
    return msg


@save_json_file(filepath=twitter_json_file, contents=TwitterFollows)
def remove_user_from_following(twitter_user: User) -> str:
    """
    Remove the user id from the following list if possible
    """
    if twitter_user.id_str in TwitterFollows:
        TwitterFollows.pop(twitter_user.id_str)
        msg = f"{twitter_user.name}(@{twitter_user.screen_name}) was removed from Subscription List."
    else:
        msg = f"You are not subscribed to{twitter_user.name}(@{twitter_user.screen_name})."
    return msg


def get_following() -> str:
    """
    Gets the list of followers and returns a list of their screen names.
    """
    if not TwitterFollows:
        msg = "You do not currently follow any Twitter Users. Use '!Follow $AccountName' to subscribe to tweets."
    else:
        msg = ',\n'.join(TwitterFollows.values())
    print(msg)
    return msg


def look_up_twitter_user(user: User) -> str:
    """
    Return the user's screen name
    """
    return f"{user.name}(@{user.screen_name})"


def get_recent_tweet_from_user(user: User):
    """
    Gets most recent tweet from a user.
    """
    format_tweet(api.user_timeline(user.id, count=1)[0])


def format_tweet(status: Status) -> None:
    """
    Gets a tweet and sends it as a webhook.
    """
    print(f"Raw tweet before any modifications: {status}")
    text = extract_text(status)
    media_links, text_media_links = get_media_links_and_remove_url(
        status, text)
    avatar = status.user.profile_image_url_https.replace("_normal.jpg", ".jpg")

    unescaped_text = unescape(text_media_links)
    print(f"Safe HTML converted to unsafe HTML: {text}")

    text_url_links = replace_tco_url_link_with_real_link(
        status, unescaped_text)
    regex = twitter_regex(text_url_links)
    send_embed_webhook(avatar=avatar, status=status,
                       link_list=media_links, text=regex)


def extract_text(status: Status) -> str:
    """
    Extracts text from Status Object.
    """
    try:
        text = status.extended_tweet["full_text"]
        print(f"Tweet is extended: {text}")

    except AttributeError:
        text = status.text
        print(f"Tweet is not extended: {text}")
    return text


def get_media_links_and_remove_url(status: Status, text: str) -> tuple:
    """
    Replaces URL's and retrieves links to media
    """
    link_list = []

    print(f"Found image in: https://twitter.com/i/web/status/{status.id}")
    try:
        # Tweet is more than 140 characters
        for image in status.extended_tweet["extended_entities"]["media"]:
            link_list.append(image["media_url_https"])
            text = text.replace(image["url"], "")
    except KeyError:
        # Tweet has no links
        pass

    except AttributeError:
        # Tweet is less than 140 characters
        try:
            for image in status.extended_entities["media"]:
                link_list.append(image["media_url_https"])
                text = text.replace(image["url"], "")
        except AttributeError:
            # Tweet has no links
            pass

    return link_list, text


def replace_tco_url_link_with_real_link(status: Status, text: str) -> str:
    """
    Replaces shortened Twitter URL
    """
    try:
        # Tweet is more than 140 characters
        for url in status.extended_tweet["entities"]["urls"]:
            text = text.replace(url["url"], url["expanded_url"])

    except AttributeError:
        # Tweet is less than 140 characters
        try:
            for url in status.entities["urls"]:
                text = text.replace(url["url"], url["expanded_url"])
        except AttributeError:
            # Tweet has no links
            pass
    return text


def twitter_regex(text: str) -> str:
    """
    Twitter URL regex using raw strings
    """
    regex_dict = {
        # Replace @username with link
        r"@(\w*)": r"[\g<0>](https://twitter.com/\g<1>)",
        # Replace #hashtag with link
        r"#(\w*)": r"[\g<0>](https://twitter.com/hashtag/\g<1>)",
        # Replace link preview with non-preview link
        r"(https://\S*)\)": r"<\g<1>>)",
        # Replace /r/subreddit with clickable link
        r".*?(/r/)([^\s^\/]*)(/|)": r"[/r/\g<2>](https://reddit.com/r/\g<2>)",
        # Replace Reddit /u/user with clickable link
        r".*?(/u/|/user/)([^\s^\/]*)(/|)": r"[/u/\g<2>](https://reddit.com/u/\g<2>)",
    }

    for pattern, replacement in regex_dict.items():
        text = sub(r"{}".format(pattern), r"{}".format(
            replacement), text, flags=MULTILINE)

    print(f"After we add links to tweet: {text}")
    return text


def send_embed_webhook(avatar: str, status, link_list, text: str):
    """
    Send tweet to Discord with Webhook
    """
    print(f"Tweet: {text}")
    hook = Webhook(Discord_Webhook)

    embed = Embed(
        description=text,
        color=0x1E0F3,
        timestamp="now",
    )
    if link_list is not None:
        if len(link_list) == 1:
            print(f"Found one image: {link_list[0]}")
            embed.set_image(link_list[0])

        elif len(link_list) > 1:
            print("Found more than one image")
            embed.set_image(link_list[0])

    embed.set_author(
        icon_url=avatar,
        name=status.user.screen_name,
        url=f"https://twitter.com/i/web/status/{status.id}",
    )

    hook.send(embed=embed)

    print("Webhook posted.")


tags = [x for x in TwitterFollows]
streamListener = MyStreamListener()
stream = Stream(auth=api.auth, listener=streamListener)
stream.filter(follow=tags, is_async=True)
