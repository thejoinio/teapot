# teapot/config.py

from environs import Env

# Initialize environs
env = Env()
env.read_env()  # This will read the .env file if it exists

# Load API keys and other environment variables
TELEGRAM_API_ID = env.str('TELEGRAM_API_ID', default='')
TELEGRAM_API_HASH = env.str('TELEGRAM_API_HASH', default='')
TELEGRAM_CHANNEL = env.str('TELEGRAM_CHANNEL', default='')
TELEGRAM_BOT = env.str('TELEGRAM_BOT', default='')
TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN', default='')

DISCORD_TOKEN = env.str('DISCORD_TOKEN', default='')
DISCORD_APP_ID = env.str('DISCORD_APP_ID', default='')
DISCORD_PUBLIC_KEY = env.str('DISCORD_PUBLIC_KEY', default='')
