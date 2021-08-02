import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

Discord_Token = os.getenv('Discord_Token', None)
Discord_Webhook = os.getenv('Discord_WebHook', None)
