import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import KEYWORD_PDF_MAPPING, BUTTONS
from pdf_handler import PDFHandler

logger = logging.getLogger(__name__)

class KeywordHandler:
    def __init__(self):
        """Initialize keyword handler with PDF handler"""
        self.pdf_handler = PDFHandler()
    
    def check_message_for_keywords(self, message_text: str) -> list:
        """Check if message contains any keywords and return matching PDFs"""
        if not message_text:
            return []
        
        message_lower = message_text.lower()
        matching_pdfs = []
        
        for keyword, pdf_filename in KEYWORD_PDF_MAPPING.items():
            if keyword.lower() in message_lower:
                matching_pdfs.append(pdf_filename)
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(matching_pdfs))
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming message and check for keywords"""
        message_text = update.message.text
        
        if not message_text:
            return False
        
        matching_pdfs = self.check_message_for_keywords(message_text)
        
        if not matching_pdfs:
            return False
        
        # Send matching PDFs
        for pdf_filename in matching_pdfs:
            await self.send_keyword_pdf(update, context, pdf_filename)
        
        return True
    
    async def send_keyword_pdf(self, update: Update, context: ContextTypes.DEFAULT_TYPE, filename: str):
        """Send PDF file based on keyword match"""
        try:
            pdf_path = self.pdf_handler.get_pdf_path(filename)
            
            if not self.pdf_handler.pdf_exists(filename):
                await update.message.reply_text(
                    f"❌ Файл {filename} не найден.\n"
                    "Пожалуйста, убедитесь, что PDF файл существует в директории pdfs."
                )
                return False
            
            # Send the PDF file with main menu button attached
            keyboard = [
                [InlineKeyboardButton(BUTTONS["main_menu"], callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            with open(pdf_path, 'rb') as pdf_file:
                await context.bot.send_document(
                    chat_id=update.message.chat_id,
                    document=pdf_file,
                    filename=filename,
                    caption=f"📄 Вот PDF файл, связанный с вашим запросом: {filename}",
                    reply_markup=reply_markup
                )
            
            logger.info(f"Keyword-triggered PDF {filename} sent to user {update.message.from_user.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending keyword PDF {filename}: {e}")
            await update.message.reply_text(
                f"❌ Ошибка при отправке {filename}. Пожалуйста, попробуйте позже."
            )
            return False 