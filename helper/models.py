from django.db import models

# Create your models here.
# helper/models.py
from django.db import models

class Email(models.Model):
    address = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
