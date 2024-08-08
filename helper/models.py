
# helper/models.py
from django.db import models

class Email(models.Model):
    address = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class TelegramMember(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    username = models.CharField(max_length=32, unique=True, null=True, blank=True)
    cached_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.phone_number})" or "Unknown Member"
