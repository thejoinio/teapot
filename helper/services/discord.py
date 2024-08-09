
import discord

from helper.models import DiscordMember

from teapot.config import DISCORD_BOT_TOKEN, DISCORD_SERVER_ID

bot_token = DISCORD_BOT_TOKEN
server_id = DISCORD_SERVER_ID

intents = discord.Intents.default()
intents.members = True
discord_client = discord.Client(intents=intents)

async def cache_server_members(members=None):
    
    try:
        if not members:
            await discord_client.login(bot_token)
            guild = discord_client.get_guild(server_id)

            async for member in guild.fetch_members():
                DiscordMember.cache_member(member)
        else:
            for member in members:
                await DiscordMember.cache_member(member)
    finally:
        await discord_client.close()
