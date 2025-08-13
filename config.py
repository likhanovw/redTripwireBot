"""
TripwireBot Configuration File
==============================

This file contains all configuration settings for the Telegram bot.
Organized into logical sections for easy maintenance and updates.
"""

import os
from dotenv import load_dotenv

# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# BOT CONFIGURATION
# =============================================================================

# Bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Validate that bot token is provided
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required. Please set it in your .env file")

# Bot identity settings
BOT_NAME = "TripwireBot"
BOT_USERNAME = "tripwire_bot"  # Change this to your bot's username

# =============================================================================
# KEYWORD MAPPING
# =============================================================================

# Maps user keywords to PDF files for automatic responses
# Format: "keyword": "filename.pdf"
KEYWORD_PDF_MAPPING = {
    # Russian keywords
    "аудит": "audit_processes.pdf",
    "процессы": "audit_processes.pdf", 
    "продукт": "audit_product.pdf",
    "продукта": "audit_product.pdf",
    "первый": "frst_file.pdf",
    "файл": "frst_file.pdf",
    
    # English keywords (for international users)
    "audit": "audit_processes.pdf",
    "processes": "audit_processes.pdf",
    "product": "audit_product.pdf",
    "first": "frst_file.pdf",
    "file": "frst_file.pdf"
}

# =============================================================================
# BOT MESSAGES
# =============================================================================

# All text messages displayed by the bot
MESSAGES = {
    # Main menu and navigation
    "welcome": "приветственное сообщение",
    "docs": "ссылки на доки",
    
    # Contact and support
    "contact_us": "вот наши контакты напишите нам",
    
    # File handling
    "brief_caption": "📋 Бриф для расчета",
    "brief_not_found": "❌ Файл бриф не найден. Обратитесь к администратору.",
    "file_error": "❌ Ошибка при отправке файла: {}",
    
    # Feature explanations
    "useful_files": """📁 Полезные файлы

Чтобы получить нужный файл, отправьте мне сообщение с ключевым словом.

**Доступные ключевые слова:**
• аудит, процессы → audit_processes.pdf
• продукт, продукта → audit_product.pdf
• первый, файл → frst_file.pdf

Просто напишите любое из этих слов, и я отправлю соответствующий PDF файл!""",
    
    # Help system
    "help": """🤖 **TripwireBot Help**

**Available Commands:**
/start - Start the bot and see available options
/help - Show this help message
/docs - Show documentation links

**How to use:**
1. Click "Start" to begin
2. Choose an option from the buttons
3. The bot will guide you through the process

**📁 Полезные файлы:**
1. Нажмите "Полезные файлы" в главном меню
2. Отправьте сообщение с ключевым словом:
   • аудит, процессы → audit_processes.pdf
   • продукт, продукта → audit_product.pdf  
   • первый, файл → frst_file.pdf
3. Получите соответствующий PDF файл

**Need more help?** Contact the bot administrator."""
}

# =============================================================================
# BUTTON CONFIGURATION
# =============================================================================

# All button texts used throughout the bot
BUTTONS = {
    # Main menu buttons
    "useful_files": "Полезные файлы",
    "calculation": "Заявка на расчет",
    
    # Navigation buttons
    "back": "Назад",
    "main_menu": "← В начало",
    "docs_back": "В начало",
    
    # Feature buttons
    "get_brief": "📋 Получить бриф",
    "contact_us": "📞 Связаться"
}

# =============================================================================
# FILE PATHS
# =============================================================================

# Important file paths used by the bot
FILES = {
    "brief": "RED.brief.odt",      # Brief file for calculations
    "user_data": "user_data.json"  # User data storage file
} 