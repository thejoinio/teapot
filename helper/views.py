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
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'status': 'error', 'message': 'phone_number is required'}, status=400)

        # check the cached data first
        phone_number = re.sub(r'\D', '', phone_number)
        phone_number_exists_in_cache = await self.get_telegram_member(phone_number)
        
        if phone_number_exists_in_cache:
            return Response({'status': 'success', 'message': 'User is part of the channel (cached)'})
        else:
            try:
                await telegram_client.start()

                phone_number_is_in_channel = False

                channel = await telegram_client.get_entity(TELEGRAM_CHANNEL)
                participants = await telegram_client.get_participants(channel)

                for participant in participants:
                    if phone_number == participant.phone:
                        phone_number_is_in_channel = True
                
                await cache_channel_members(participants)

                if phone_number_is_in_channel:
                    return Response({'status': 'success', 'message': 'User is part of the channel'})
                else:
                    Response({'status': 'error', 'message': 'User is not part of the channel'}, status=404)

            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=400)
            finally:
                telegram_client.disconnect()

        return Response({'status': 'error', 'message': 'User is not part of the channel'}, status=404)
    
    @sync_to_async
    def get_telegram_member(self, phone_number):
        return TelegramMember.objects.filter(phone_number=phone_number).exists()

class VerifyDiscordView(APIView):
    
    async def post(self, request):
        discord_tag = request.data.get('discord_tag')
        if not discord_tag:
            return Response({'status': 'error', 'message': 'discord_tag is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check cached data first
        member_exists_in_cache = await self.member_exists_in_cache(discord_tag)

        if member_exists_in_cache:
            return Response({'status': 'success', 'message': f'{discord_tag} is a member of the server (cached)'})
        else:
            try:
                await discord_client.login(discord_bot_token)

                member_is_in_server = False

                guild = await self.get_discord_guild()

                if not guild:
                    raise Exception("cannot find discord server")
                
                members = [member async for member in guild.fetch_members()]
                    
                for member in members:
                    if member.name == discord_tag:
                        member_is_in_server = True
                        break
                
                await cache_server_members(members)

                if member_is_in_server:
                    return Response({'status': 'success', 'message': f'{discord_tag} is a member of the server'})
                else:
                    return Response({'status': 'error', 'message': f'{discord_tag} is not a member of the server'}, status=status.HTTP_400_BAD_REQUEST)
            
            except Exception as e:
                raise
                return Response({'status': 'error', 'message': str(e)}, status=400)
            finally:
                await discord_client.close()

        return Response({'status': 'error', 'message': f'{discord_tag} is not a member of the server'}, status=status.HTTP_400_BAD_REQUEST)

    async def get_discord_guild(self):
        await discord_client.login(discord_bot_token)

        guilds = [guild async for guild in discord_client.fetch_guilds(limit=150)]
        
        for guild in guilds:
            if guild.id == discord_server_id:
                return guild
        
        return None

    @sync_to_async
    def member_exists_in_cache(self, discord_tag):
        return DiscordMember.objects.filter(name=discord_tag).exists()
