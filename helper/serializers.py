# helper/serializers.py
from rest_framework import serializers
from .models import Email, JoindaAccount

class EmailSerializer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=2, required=False)  # Optional country field
    campaign = serializers.CharField(max_length=20, required=True)  # Optional campaign field
    discord_username = serializers.CharField(max_length=32, required=False)  # Optional Discord username
    class Meta:
        model = Email
        fields = ['id', 'address', 'created_at', 'country', 'campaign', 'discord_username']

class JoindaAccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=32, required=True)
    gender = serializers.CharField(max_length=10, required=True)
    discord_username = serializers.CharField(max_length=100, required=False)
    class Meta:
        model = JoindaAccount
        fields = ['email', 'username', 'gender', 'discord_username']
