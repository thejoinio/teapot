# helper/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Email
from .serializers import EmailSerializer

from telethon import TelegramClient
from discord import Intents, Client

from teapot.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_CHANNEL, DISCORD_TOKEN

telegram_client = TelegramClient('session_name', TELEGRAM_API_ID, TELEGRAM_API_HASH)

intents = Intents.default()
intents.message_content = True
discord_client = Client(intents=intents)


class SubmitEmailView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'email': serializer.data['address']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyTelegramView(APIView):
    def post(self, request):
        identifier = request.data.get('identifier')
        if identifier:
            telegram_client.start()

            try:
                participant = telegram_client.get_participant(TELEGRAM_CHANNEL, identifier)
                if participant:
                    return Response({'status': 'success', 'message': 'User is part of the channel'})
                else:
                    return Response({'status': 'error', 'message': 'User is not part of the channel'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'error', 'message': 'Identifier is required'}, status=status.HTTP_400_BAD_REQUEST)

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
