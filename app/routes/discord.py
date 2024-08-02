from starlette.requests import Request
from starlette.responses import JSONResponse
from discord import Intents, Client
from ..config import DISCORD_TOKEN

intents = Intents.default()
intents.message_content = True

discord_client = Client(intents=intents)

async def verify_discord(request: Request):
    data = await request.json()
    discord_tag = data.get('discord_tag')

    if not discord_tag:
        return JSONResponse({'status': 'error', 'message': 'Discord tag is required'}, status_code=400)

    @discord_client.event
    async def on_ready():
        for guild in discord_client.guilds:
            member = guild.get_member_named(discord_tag)
            if member:
                return JSONResponse({'status': 'success', 'message': f'{discord_tag} is part of the guild'})
        await discord_client.close()

    await discord_client.start(DISCORD_TOKEN)

    return JSONResponse({'status': 'error', 'message': f'{discord_tag} is not part of the guild'}, status_code=404)
