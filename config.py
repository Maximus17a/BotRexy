import os
from dotenv import load_dotenv

load_dotenv()

# Discord Bot Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
BOT_PREFIX = '!'

# Web Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/callback')
WEB_PORT = int(os.getenv('PORT', 5000))

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Bot Settings
XP_PER_MESSAGE = 15
XP_COOLDOWN = 60  # seconds
LEVEL_MULTIPLIER = 100

# Automod Settings
MAX_MENTIONS = 5
MAX_EMOJIS = 10
SPAM_THRESHOLD = 5  # messages
SPAM_INTERVAL = 5  # seconds

# Discord OAuth2
DISCORD_API_BASE = 'https://discord.com/api/v10'
OAUTH2_SCOPES = ['identify', 'guilds']
