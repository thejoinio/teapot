# Generated by Django 5.1.4 on 2024-12-17 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0006_email_discord_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoindaAccount',
            fields=[
                ('discord_username', models.CharField(max_length=100, unique=True)),
                ('discord_member_id', models.CharField(db_column='member_id', max_length=20, primary_key=True, serialize=False)),
                ('is_discord_bot', models.BooleanField(default=False)),
                ('discord_nick', models.CharField(blank=True, max_length=100, null=True)),
                ('username', models.CharField(max_length=100)),
                ('email', models.CharField(unique=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
