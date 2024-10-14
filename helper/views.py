# helper/views.py

import os
from asgiref.sync import sync_to_async

from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .models import TelegramMember, DiscordMember
from .serializers import EmailSerializer

import markdown, requests
from adrf.views import APIView

from teapot.config import TELEGRAM_CHANNEL, DISCORD_BOT_TOKEN, DISCORD_SERVER_ID,\
      ZEPTOMAIL_TEMPLATE_ALIAS, ZEPTOMAIL_SENDMAIL_TOKEN, ZEPTOMAIL_SENDER, \
      ZEPTOMAIL_SENDER_ADDRESS, CAMPAIGN_CODES
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
    VALID_CAMPAIGNS = CAMPAIGN_CODES

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email_address = serializer.validated_data['address']
            country = serializer.validated_data.get('country', None)  # Optional country
            campaign = serializer.validated_data.get('campaign', None)  # Optional campaign
            discord_username = serializer.validated_data.get('discord_username', None) # Optional Discord username

            # Validate the country (ISO 3166-1 alpha-2)
            if country and len(country) != 2:
                return Response({'status': 'error', 'message': 'Invalid country code. Must be a 2-letter code.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Validate the campaign against valid campaign codes
            if campaign and campaign not in self.VALID_CAMPAIGNS:
                return Response({'status': 'error', 'message': 'Invalid campaign code.'},
                                status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            # Send welcome email using ZeptoMail Template API
            zepto_mail_template_alias = ZEPTOMAIL_TEMPLATE_ALIAS
            zepto_mail_sendmail_token = ZEPTOMAIL_SENDMAIL_TOKEN
            zepto_mail_api_url = 'https://api.zeptomail.com/v1.1/email/template'

            # Add the optional fields to the merge_info if provided
            merge_info = {}
            if country:
                merge_info['country'] = country
            if campaign:
                merge_info['campaign'] = campaign

            payload = {
                'from': {
                    'address': ZEPTOMAIL_SENDER_ADDRESS,
                    'name': ZEPTOMAIL_SENDER
                },
                'to': [
                    {
                        'email_address': {
                            'address': email_address,
                        }
                    }
                ],
                'template_alias': zepto_mail_template_alias,
                'merge_info': merge_info
            }

            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': zepto_mail_sendmail_token
            }

            # Make POST request to ZeptoMail API
            try:
                response = requests.post(zepto_mail_api_url, json=payload, headers=headers)
                if response.status_code == 201:
                    return Response({'status': 'success', 'email': email_address}, status=status.HTTP_201_CREATED)
                else:
                    payload = {
                        'status': 'error',
                        'message': 'Failed to send email. Please try again later.',
                        'error': response.json()['error'] if settings.DEBUG else 'Failed to send email. Please try again later.'
                    }
                    return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
