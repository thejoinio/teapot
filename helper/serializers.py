# helper/serializers.py
from rest_framework import serializers
from .models import Email

class EmailSerializer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=2, required=False)  # Optional country field
    campaign = serializers.CharField(max_length=10, required=False)  # Optional campaign field
    discord_username = serializers.CharField(max_length=32, required=False)  # Optional Discord username
    class Meta:
        model = Email
        fields = ['id', 'address', 'created_at', 'country', 'campaign', 'discord_username']
