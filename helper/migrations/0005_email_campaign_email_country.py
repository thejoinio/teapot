# Generated by Django 5.1 on 2024-10-13 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0004_discordmember'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='campaign',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='email',
            name='country',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
