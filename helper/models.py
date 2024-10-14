# helper/models.py

from asgiref.sync import sync_to_async

from django.db import models
from django.utils import timezone

class Email(models.Model):
    address = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=2, null=True, blank=True)  # Optional two-letter country code
    campaign = models.CharField(max_length=10, null=True, blank=True)  # Optional campaign code
    discord_username = models.CharField(max_length=32, null=True, blank=True) # Optional Discord username

    def __str__(self):
        return self.address

class TelegramMember(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    username = models.CharField(max_length=32, unique=True, null=True, blank=True)
    cached_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.phone_number})" or "Unknown Member"

class DiscordMember(models.Model):
    member_id = models.CharField(max_length=20, primary_key=True, db_column='member_id')  # Stored as 'member_id' in the DB
    name = models.CharField(max_length=100)
    bot = models.BooleanField(default=False)
    nick = models.CharField(max_length=100, null=True, blank=True)
    cached_at = models.DateTimeField()

    def __str__(self):
        return f"{self.name} ({'Bot' if self.bot else 'User'})"

    @classmethod
    @sync_to_async
    def cache_member(cls, member):
        """
        Cache or update a Discord member in the database.

        :param member: An object with properties that match Discord member fields.
                       Expected to have `id`, `name`, `bot`, and `nick`.
        """
        obj, created = cls.objects.update_or_create(
            member_id=member.id,  # Using member.id here as that's what Discord provides
            defaults={
                'name': member.name,
                'bot': member.bot,
                'nick': member.nick or '',
                'cached_at': timezone.now()
            }
        )
        return obj
