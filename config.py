import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
ABUSE_IPDB_KEY = os.getenv('ABUSE_IPDB_KEY')
WHOIS_API_KEY = os.getenv('WHOIS_API_KEY')
EMAIL_FINDER_KEY = os.getenv('EMAIL_FINDER_KEY')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
WORKERS = int(os.getenv('WORKERS', 4))