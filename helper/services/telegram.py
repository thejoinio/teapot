# helper/telegram_client.py

import asyncio
# from subprocess import check_output

from telethon import TelegramClient

from helper.models import TelegramMember

from teapot.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_CHANNEL

api_id = TELEGRAM_API_ID
api_hash = TELEGRAM_API_HASH
channel_id = TELEGRAM_CHANNEL

telethon_service_id = "teapot-service"

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
client = TelegramClient(telethon_service_id, api_id, api_hash, loop=loop)

async def cache_channel_members(participants=None):
    try:
        if not participants:
            channel = await client.get_entity(channel_id)
            participants = await client.get_participants(channel)
        await TelegramMember.objects.all().adelete()  # Clear existing cached data
        members_to_add = []
        for p in participants:
            if p.phone or p.username:  # Ensure we have at least one piece of identifiable information
                members_to_add.append(TelegramMember(phone_number=p.phone, username=p.username))
        await TelegramMember.objects.abulk_create(members_to_add)
    finally:
        await client.disconnect()
