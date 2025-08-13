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

# Keyword to PDF mapping for automatic responses
KEYWORD_PDF_MAPPING = {
    "аудит": "audit_processes.pdf",
    "процессы": "audit_processes.pdf", 
    "продукт": "audit_product.pdf",
    "продукта": "audit_product.pdf",
    "первый": "frst_file.pdf",
    "файл": "frst_file.pdf",
    "audit": "audit_processes.pdf",
    "processes": "audit_processes.pdf",
    "product": "audit_product.pdf",
    "first": "frst_file.pdf",
    "file": "frst_file.pdf"
} 