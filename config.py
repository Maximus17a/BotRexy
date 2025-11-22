import os
from dotenv import load_dotenv

load_dotenv()

# Web Configuration
# SECURITY: Fail if SECRET_KEY is not set in production
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application")

REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/callback')
WEB_PORT = int(os.getenv('PORT', 5000))

# SECURITY: Session Cookies
SESSION_COOKIE_SECURE = True  # Require HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent XSS access to cookies
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection

# SECURITY: Max File Upload Size (5MB)
MAX_CONTENT_LENGTH = 5 * 1024 * 1024

# Discord Bot Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
BOT_PREFIX = '!'

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Bot Settings
XP_PER_MESSAGE = 15
XP_COOLDOWN = 60
LEVEL_MULTIPLIER = 100

# Automod Settings
MAX_MENTIONS = 5
MAX_EMOJIS = 10
SPAM_THRESHOLD = 5
SPAM_INTERVAL = 5

# Discord OAuth2
DISCORD_API_BASE = 'https://discord.com/api/v10'
OAUTH2_SCOPES = ['identify', 'guilds']