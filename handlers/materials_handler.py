import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class MaterialsHandler:
    """Handler for useful materials functionality"""
    
    def __init__(self, pdf_handler):
        self.pdf_handler = pdf_handler
    
    async def handle_materials_request(self, query, context):
        """Handle materials request"""
        keyboard = [
            [InlineKeyboardButton("первый файл", callback_data="materials_file_1")],
            [InlineKeyboardButton("второй файл", callback_data="materials_file_2")],
            [InlineKeyboardButton("третий файл", callback_data="materials_file_3")],
            [InlineKeyboardButton("Назад", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выбор материала из списка", reply_markup=reply_markup)
    
    async def handle_materials_file_1(self, query, context):
        """Handle first materials file"""
        try:
            # Create a mock Update object for the pdf_handler
            from telegram import Update
            mock_update = Update(0, callback_query=query)
            await self.pdf_handler.send_pdf(mock_update, context, "frst_file.pdf")
        except Exception as e:
            logger.error(f"Error sending first materials file: {e}")
            keyboard = [
                [InlineKeyboardButton("Назад", callback_data="materials")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("❌ Ошибка отправки файла. Попробуйте позже.", reply_markup=reply_markup)
    
    async def handle_materials_file_2(self, query, context):
        """Handle second materials file"""
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="materials")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📄 Второй файл: функциональность в разработке", reply_markup=reply_markup)
    
    async def handle_materials_file_3(self, query, context):
        """Handle third materials file"""
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="materials")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📄 Третий файл: функциональность в разработке", reply_markup=reply_markup) 