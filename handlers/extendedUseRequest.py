import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class ExtendedUseRequestHandler:
    """Handler for extended use requests including audit functionality"""
    
    def __init__(self, pdf_handler):
        self.pdf_handler = pdf_handler
    
    async def handle_has_product(self, query, context):
        """Handle 'Есть продукт' selection"""
        keyboard = [
            [InlineKeyboardButton("Своя команда", callback_data="own_team")],
            [InlineKeyboardButton("Аутстафф", callback_data="outstaff")],
            [InlineKeyboardButton("Аутсорс", callback_data="outsource")],
            [InlineKeyboardButton("Нет никого", callback_data="no_team")],
            [InlineKeyboardButton("Назад", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("✅ Есть продукт: выберите опцию", reply_markup=reply_markup)
    
    async def handle_no_product(self, query, context):
        """Handle 'Нет продукта' selection"""
        keyboard = [
            [InlineKeyboardButton("полностью сами", callback_data="fully_own")],
            [InlineKeyboardButton("Сами + усиление извне", callback_data="own_plus_external")],
            [InlineKeyboardButton("Заказная разработка", callback_data="custom_development")],
            [InlineKeyboardButton("Покупка готового продукта с кастомизацией", callback_data="buy_customize")],
            [InlineKeyboardButton("Назад", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("❌ Нет продукта: выберите опцию", reply_markup=reply_markup)
    
    async def handle_own_team(self, query, context):
        """Handle 'Своя команда' selection"""
        keyboard = [
            [InlineKeyboardButton("Аудит процессов + рекомендация проджекта", callback_data="audit_processes")],
            [InlineKeyboardButton("Аудит продукта + рекоммендации продакта", callback_data="audit_product")],
            [InlineKeyboardButton("Назад", callback_data="back_to_has_product")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("👥 Своя команда: выберите опцию", reply_markup=reply_markup)
    
    async def handle_outstaff(self, query, context):
        """Handle 'Аутстафф' selection"""
        keyboard = [
            [InlineKeyboardButton("аудит работы привлеченных специалистов + рекомендации проджекта и/или HR", callback_data="audit_outstaff_specialists")],
            [InlineKeyboardButton("Аудит продукта + рекоммендации продакта", callback_data="audit_product")],
            [InlineKeyboardButton("Назад", callback_data="back_to_has_product")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("👨‍💼 Аутстафф: выберите опцию", reply_markup=reply_markup)
    
    async def handle_other_team_options(self, query, context):
        """Handle other team options (outsource, no_team)"""
        responses = {
            "outsource": "🏢 Аутсорс: выберите опцию",
            "no_team": "🚫 Нет никого: выберите опцию"
        }
        await query.edit_message_text(responses[query.data])
    
    async def handle_back_to_has_product(self, query, context):
        """Handle 'Назад' to 'Есть продукт' menu"""
        keyboard = [
            [InlineKeyboardButton("Своя команда", callback_data="own_team")],
            [InlineKeyboardButton("Аутстафф", callback_data="outstaff")],
            [InlineKeyboardButton("Аутсорс", callback_data="outsource")],
            [InlineKeyboardButton("Нет никого", callback_data="no_team")],
            [InlineKeyboardButton("Назад", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("✅ Есть продукт: выберите опцию", reply_markup=reply_markup)
    
    async def handle_audit_options(self, query, context):
        """Handle audit options - send PDF files"""
        pdf_files = {
            "audit_processes": "audit_processes.pdf",
            "audit_product": "audit_product.pdf",
            "audit_outstaff_specialists": "audit_outstaff_specialists.pdf"
        }
        
        if query.data in pdf_files:
            filename = pdf_files[query.data]
            try:
                await self.pdf_handler.send_pdf(query, context, filename)
            except Exception as e:
                logger.error(f"Error sending PDF {filename}: {e}")
                await query.edit_message_text(f"❌ Ошибка отправки файла {filename}. Попробуйте позже.")
    
    async def handle_no_product_options(self, query, context):
        """Handle no product options"""
        responses = {
            "fully_own": "🛠️ Полностью сами: выберите опцию",
            "own_plus_external": "🔧 Сами + усиление извне: выберите опцию",
            "custom_development": "📋 Заказная разработка: выберите опцию",
            "buy_customize": "🛒 Покупка готового продукта с кастомизацией: выберите опцию"
        }
        await query.edit_message_text(responses[query.data])
    
    async def handle_back_to_start(self, query, context):
        """Handle 'Назад' to main menu"""
        keyboard = [
            [InlineKeyboardButton("Заявка на расчет", callback_data="calculation")],
            [InlineKeyboardButton("Заявка на стратегическую сессию", callback_data="strategic")],
            [InlineKeyboardButton("Полезные материалы", callback_data="materials")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # If message has a document, send new message. Otherwise, edit existing message
        if query.message.document:
            # PDF message - send new message
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text="приветственное сообщение",
                reply_markup=reply_markup
            )
        else:
            # Regular text message - edit existing message
            await query.edit_message_text("приветственное сообщение", reply_markup=reply_markup) 