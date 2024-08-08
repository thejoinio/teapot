# helper/views.py

import re, os
from asgiref.sync import sync_to_async

# from rest_framework.views import APIView
from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from .models import TelegramMember
from .serializers import EmailSerializer

import markdown
from adrf.views import APIView
from discord import Intents, Client

from teapot.config import TELEGRAM_CHANNEL, TELEGRAM_BOT_TOKEN, DISCORD_TOKEN
from .services.telegram import client, cache_channel_members

intents = Intents.default()
intents.members = True
intents.guilds = True
discord_client = Client(intents=intents)


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
            return Response({'status': 'error', 'message': 'Phone number is required'}, status=400)

        # Check the cached data first
        phone_number = re.sub(r'\D', '', phone_number)
        phone_number_exists_in_cache = await self.get_telegram_member(phone_number)
        
        if phone_number_exists_in_cache:
            return Response({'status': 'success', 'message': 'User is part of the channel (cached)'})
        else:
            try:
                await client.start(bot_token=TELEGRAM_BOT_TOKEN)

                phone_number_is_in_channel = False

                channel = await client.get_entity(TELEGRAM_CHANNEL)
                participants = await client.get_participants(channel)

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
        return Response({'status': 'error', 'message': 'User is not part of the channel'}, status=404)
    
    @sync_to_async
    def get_telegram_member(self, phone_number):
        return TelegramMember.objects.filter(phone_number=phone_number).exists()

class VerifyDiscordView(APIView):
    def post(self, request):
        discord_tag = request.data.get('discord_tag')
        if discord_tag:

            for guild in discord_client.guilds:
                member = guild.get_member_named(discord_tag)
                if member:
                    return Response({'status': 'success', 'message': f'{discord_tag} is part of the guild'})
            discord_client.close()

            discord_client.start(DISCORD_TOKEN)

            return Response({'status': 'error', 'message': f'{discord_tag} is not part of the guild'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'error', 'message': 'Discord tag is required'}, status=status.HTTP_400_BAD_REQUEST)
