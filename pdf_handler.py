import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class PDFHandler:
    def __init__(self, pdf_directory="pdfs"):
        """Initialize PDF handler with directory for PDF files"""
        self.pdf_directory = pdf_directory
        self.ensure_pdf_directory()
    
    def ensure_pdf_directory(self):
        """Create PDF directory if it doesn't exist"""
        if not os.path.exists(self.pdf_directory):
            os.makedirs(self.pdf_directory)
            logger.info(f"Created PDF directory: {self.pdf_directory}")
    
    def get_pdf_path(self, filename):
        """Get full path to PDF file"""
        return os.path.join(self.pdf_directory, filename)
    
    def pdf_exists(self, filename):
        """Check if PDF file exists"""
        return os.path.exists(self.get_pdf_path(filename))
    
    async def send_pdf(self, update: Update, context: ContextTypes.DEFAULT_TYPE, filename):
        """Send PDF file to user"""
        try:
            pdf_path = self.get_pdf_path(filename)
            
            if not self.pdf_exists(filename):
                await update.callback_query.edit_message_text(
                    f"❌ File {filename} not found.\n\n"
                    "Please ensure the PDF file exists in the pdfs directory."
                )
                return False
            
            # Send the PDF file
            with open(pdf_path, 'rb') as pdf_file:
                await context.bot.send_document(
                    chat_id=update.callback_query.from_user.id,
                    document=pdf_file,
                    filename=filename,
                    caption=f"📄 Держите {filename}"
                )
            
            # Update the original message with main menu button
            keyboard = [
                [InlineKeyboardButton("Главное меню", callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.edit_message_text(
                f"✅ {filename} отправлен успешно!", reply_markup=reply_markup
            )
            
            logger.info(f"PDF {filename} sent to user {update.callback_query.from_user.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending PDF {filename}: {e}")
            await update.callback_query.edit_message_text(
                f"❌ Error sending {filename}. Please try again later."
            )
            return False
    
    def list_available_pdfs(self):
        """List all available PDF files in the directory"""
        if not os.path.exists(self.pdf_directory):
            return []
        
        pdf_files = []
        for file in os.listdir(self.pdf_directory):
            if file.lower().endswith('.pdf'):
                pdf_files.append(file)
        
        return pdf_files 