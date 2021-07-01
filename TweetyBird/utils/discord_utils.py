import aiohttp

from discord import Webhook, AsyncWebhookAdapter

from utils.settings import Discord_Webhook


async def send_discord_message(message):
    """
    Sends a message to a discord server/room through a webhook.
    """
    async with aiohttp.ClientSession as session:
        webhook = Webhook.from_url(Discord_Webhook, adapter=AsyncWebhookAdapter(session))
        await webhook.send(message)