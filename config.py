import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Validate that bot token is provided
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required. Please set it in your .env file")

# Bot settings
BOT_NAME = "TripwireBot"
BOT_USERNAME = "tripwire_bot"  # Change this to your bot's username 