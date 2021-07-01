import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

Discord_Token = os.getenv('Discord_Token', None)
Twitter_API_PK = os.getenv('Twitter_API_PK', None)
Twitter_API_SK = os.getenv('Twitter_API_SK', None)
Twitter_Access_Token = os.getenv('Twitter_Access_Token', None)
Twitter_Access_Secret = os.getenv('Twitter_Access_Secret', None)
Discord_Webhook = os.getenv('Discord_WebHook', None)
