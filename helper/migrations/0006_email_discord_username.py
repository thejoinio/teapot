# Generated by Django 5.1 on 2024-10-14 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0005_email_campaign_email_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='discord_username',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
