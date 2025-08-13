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

# Bot messages
MESSAGES = {
    "welcome": "приветственное сообщение",
    "docs": "ссылки на доки",
    "contact_us": "вот наши контакты напишите нам",
    "brief_caption": "📋 Бриф для расчета",
    "brief_not_found": "❌ Файл бриф не найден. Обратитесь к администратору.",
    "file_error": "❌ Ошибка при отправке файла: {}",
    "useful_files": """📁 Полезные файлы

Чтобы получить нужный файл, отправьте мне сообщение с ключевым словом.

**Доступные ключевые слова:**
• аудит, процессы → audit_processes.pdf
• продукт, продукта → audit_product.pdf
• первый, файл → frst_file.pdf

Просто напишите любое из этих слов, и я отправлю соответствующий PDF файл!""",
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

# Button texts
BUTTONS = {
    "useful_files": "Полезные файлы",
    "calculation": "Заявка на расчет",
    "back": "Назад",
    "main_menu": "← В начало",
    "get_brief": "📋 Получить бриф",
    "contact_us": "📞 Связаться",
    "docs_back": "В начало"
}

# File paths
FILES = {
    "brief": "RED.brief.odt",
    "user_data": "user_data.json"
} 