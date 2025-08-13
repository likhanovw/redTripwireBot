import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class CalculationHandler:
    """Handler for calculation application functionality"""
    
    def __init__(self, pdf_handler):
        self.pdf_handler = pdf_handler
    
    async def handle_calculation_request(self, query, context):
        """Handle calculation request"""
        keyboard = [
            [InlineKeyboardButton("📋 Получить бриф", callback_data="get_brief")],
            [InlineKeyboardButton("📞 Связаться", callback_data="contact_us")],
            [InlineKeyboardButton("Назад", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Check if the message has a document (PDF) - can't edit those
        if query.message.document:
            # Document message - send new message instead of editing
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text="🧮 Заявка на расчет\n\nФункциональность в разработке.",
                reply_markup=reply_markup
            )
        else:
            # Regular text message - edit existing message
            await query.edit_message_text("🧮 Заявка на расчет\n\nФункциональность в разработке.", reply_markup=reply_markup) 