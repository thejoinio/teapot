# helper/views.py

import re, os
from asgiref.sync import sync_to_async

from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from .models import TelegramMember, DiscordMember
from .serializers import EmailSerializer

import markdown
from adrf.views import APIView

from teapot.config import TELEGRAM_CHANNEL, DISCORD_BOT_TOKEN, DISCORD_SERVER_ID
from .services.telegram import telegram_client, cache_channel_members
from .services.discord import discord_client, cache_server_members

discord_bot_token = DISCORD_BOT_TOKEN
discord_server_id = DISCORD_SERVER_ID


def render_markdown_page(request, page_name):
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    file_path = os.path.join(static_dir, f"{page_name}.md")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        html_content = markdown.markdown(content)
    except FileNotFoundError:
        raise Http404("Page not found")

    return render(request, 'helper/markdown.html', {
        'content': html_content,
        'title': page_name.capitalize()
    })

class SubmitEmailView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'email': serializer.data['address']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyTelegramView(APIView):
    
    async def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({'status': 'error', 'message': 'username is required'}, status=400)

        # check the cached data first
        username_exists_in_cache = await self.get_telegram_member(username)
        
        if username_exists_in_cache:
            return Response({'status': 'success', 'message': f'{username} is a member of the channel', 'source': 'cache'})
        else:
            try:
                await telegram_client.start()

                username_is_in_channel = False

                channel = await telegram_client.get_entity(TELEGRAM_CHANNEL)
                participants = await telegram_client.get_participants(channel)

                for participant in participants:
                    if username == participant.username:
                        username_is_in_channel = True
                
                await cache_channel_members(participants)

                if username_is_in_channel:
                    telegram_client.disconnect()
                    return Response({'status': 'success', 'message': f'{username} is a member of the channel', 'source': 'telegram'})
                else:
                    telegram_client.disconnect()
                    return Response({'status': 'error', 'message': f'{username} is not a member of the channel'}, status=404)

            except Exception as e:
                telegram_client.disconnect()
                return Response({'status': 'error', 'message': str(e)}, status=400)
            finally:
                telegram_client.disconnect()
    
    @sync_to_async
    def get_telegram_member_by_phone(self, phone_number):
        return TelegramMember.objects.filter(phone_number=phone_number).exists()
    
    @sync_to_async
    def get_telegram_member(self, username):
        return TelegramMember.objects.filter(username=username).exists()

class VerifyDiscordView(APIView):
    
    async def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({'status': 'error', 'message': 'username is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check cached data first
        member_exists_in_cache = await self.member_exists_in_cache(username)

        if member_exists_in_cache:
            return Response({'status': 'success', 'message': f'{username} is a member of the server', 'source': 'cache'})
        else:
            try:
                await discord_client.login(discord_bot_token)

                member_is_in_server = False

                guild = await self.get_discord_guild()

                if not guild:
                    raise Exception("cannot find discord server")
                
                members = [member async for member in guild.fetch_members()]
                    
                for member in members:
                    if member.name == username:
                        member_is_in_server = True
                        break
                
                await cache_server_members(members)

                if member_is_in_server:
                    discord_client.close()
                    return Response({'status': 'success', 'message': f'{username} is a member of the server', 'source': 'discord'})
                else:
                    discord_client.close()
                    return Response({'status': 'error', 'message': f'{username} is not a member of the server'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                discord_client.close()
                return Response({'status': 'error', 'message': str(e)}, status=400)
            finally:
                await discord_client.close()

    async def get_discord_guild(self):
        await discord_client.login(discord_bot_token)

        guilds = [guild async for guild in discord_client.fetch_guilds(limit=150)]
        
        for guild in guilds:
            if guild.id == discord_server_id:
                return guild
        
        return None

    @sync_to_async
    def member_exists_in_cache(self, username):
        return DiscordMember.objects.filter(name=username).exists()
