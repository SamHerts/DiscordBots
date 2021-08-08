import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

Discord_Token = os.getenv('BT_Discord_Token', None)
BT_Discord_Webhook = os.getenv('Discord_WebHook', None)
