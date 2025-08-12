import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ForceReply
from telegram.ext import ContextTypes
from datetime import datetime

logger = logging.getLogger(__name__)

class DataCollectionHandler:
    """Handler for user data collection with consent"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    async def request_initial_consent(self, update, context):
        """Request initial consent when user first starts the bot"""
        consent_text = """
📋 Добро пожаловать!

Для предоставления качественных услуг нам необходимо обрабатывать ваши персональные данные:
• Имя
• Номер телефона

Данные хранятся в защищенном виде и используются только для связи с вами.

Согласны ли вы на обработку персональных данных?
        """
        
        keyboard = [
            [InlineKeyboardButton("✅ Согласен", callback_data="consent_yes")],
            [InlineKeyboardButton("❌ Не согласен", callback_data="consent_no")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(consent_text, reply_markup=reply_markup)
    
    async def request_consent(self, query, context):
        """Request permission to process personal data"""
        consent_text = """
📋 Согласие на обработку персональных данных

Для предоставления услуг нам необходимо обрабатывать ваши персональные данные:
• Имя
• Номер телефона  
• Информация о проекте

Данные хранятся в защищенном виде и используются только для связи с вами.

Согласны ли вы на обработку персональных данных?
        """
        
        keyboard = [
            [InlineKeyboardButton("✅ Согласен", callback_data="consent_yes")],
            [InlineKeyboardButton("❌ Не согласен", callback_data="consent_no")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Check if the message has a document (PDF) - can't edit those
        if query.message.document:
            # PDF message - send new message instead of editing
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text=consent_text,
                reply_markup=reply_markup
            )
        else:
            # Regular text message - edit existing message
            await query.edit_message_text(consent_text, reply_markup=reply_markup)
    
    async def handle_consent_yes(self, query, context):
        """User agreed to data processing"""
        user = query.from_user
        
        # Collect basic data automatically
        user_data = {
            "telegram_id": user.id,
            "name": None,  # Will be collected from contact
            "username": user.username,
            "phone": None,  # Will be collected via contact sharing
            "consent_given": True,
            "consent_date": datetime.now().isoformat()
        }
        
        # Save to JSON
        if self.data_manager.save_user_data(user.id, user_data):
            # Request contact information directly
            keyboard = [
                [InlineKeyboardButton("📱 Поделиться", callback_data="request_contact")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "Спасибо! Теперь предоставьте ваш номер телефона для связи:",
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text("❌ Ошибка сохранения данных. Попробуйте позже.")
    
    async def handle_consent_no(self, query, context):
        """User declined data processing"""
        keyboard = [
            [InlineKeyboardButton("🔄 Попробовать снова", callback_data="consent_yes")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Понятно! Без согласия мы не можем обрабатывать ваши данные.\n"
            "Вы всегда можете изменить свое решение позже.",
            reply_markup=reply_markup
        )
    
    async def request_contact(self, query, context):
        """Request contact information"""
        keyboard = [
            [KeyboardButton("📱 Поделиться", request_contact=True)]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text="Пожалуйста, нажмите кнопку 'Поделиться' для предоставления вашего номера телефона:",
            reply_markup=reply_markup
        )
    
    async def handle_phone_shared(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle when user shares their phone number"""
        if update.message.contact:
            user_id = update.message.from_user.id
            contact = update.message.contact
            phone = contact.phone_number
            name = contact.first_name or contact.full_name or "Не указано"
            
            # Update user data with both name and phone from contact
            user_data = self.data_manager.get_user_data(user_id)
            if user_data:
                user_data["data"]["phone"] = phone
                user_data["data"]["name"] = name
                user_data["data"]["last_updated"] = datetime.now().isoformat()
                self.data_manager.save_user_data(user_id, user_data["data"])
            
            # Go directly to new feature after data collection
            await update.message.reply_text(
                f"Спасибо! Ваше имя: {name}\nВаш номер: {phone}\n\n"
                f"Данные успешно сохранены. Мы свяжемся с вами в ближайшее время!"
            )
            
            # Send new feature directly
            keyboard = [
                [InlineKeyboardButton("🆕 Начать новую функцию", callback_data="new_feature")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Готовы начать работу с новой функцией?",
                reply_markup=reply_markup
            )
    

    

    
    async def show_user_data(self, query, context):
        """Show collected user data (for testing)"""
        user_id = query.from_user.id
        user_data = self.data_manager.get_user_data(user_id)
        
        if user_data:
            data = user_data["data"]
            stats = self.data_manager.get_stats()
            
            message = f"""
📊 Ваши данные:
Имя: {data.get('name', 'Не указано')}
Телефон: {data.get('phone', 'Не указан')}
Username: {data.get('username', 'Не указан')}
Дата согласия: {user_data.get('consent_date', 'Не указана')}

📈 Статистика:
Всего пользователей: {stats['total_users']}
Согласились: {stats['users_with_consent']}
Процент согласия: {stats['consent_rate']:.1f}%
            """
        else:
            message = "У вас пока нет сохраненных данных."
        
        keyboard = [
            [InlineKeyboardButton("Главное меню", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup) 