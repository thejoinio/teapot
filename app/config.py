from environs import Env

env = Env()
env.read_env()  # read .env file, if present

# Load variables from environment
DATABASE_URL = env.str("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")
API_ID = env.str("TELEGRAM_API_ID")
API_HASH = env.str("TELEGRAM_API_HASH")
CHANNEL = env.str("TELEGRAM_CHANNEL")
DISCORD_TOKEN = env.str("DISCORD_TOKEN")
