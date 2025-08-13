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
        
        # Force reload data to get the latest user data
        self.data_manager.reload_data()
        
        # Small delay to ensure file is written
        import time
        time.sleep(0.1)
        
        # Check if user already exists in our database
        existing_user_data = self.data_manager.get_user_data(user.id)
        
        # Debug logging
        logger.info(f"User {user.id} existing data: {existing_user_data}")
        
        # Check if user has phone number (either in data or directly in user_data)
        has_phone = False
        if existing_user_data:
            # Check in the data object
            if existing_user_data.get("data", {}).get("phone"):
                has_phone = True
                logger.info(f"User {user.id} has phone in data: {existing_user_data.get('data', {}).get('phone')}")
            # Also check if phone is directly in user_data (for backward compatibility)
            elif existing_user_data.get("phone"):
                has_phone = True
                logger.info(f"User {user.id} has phone directly: {existing_user_data.get('phone')}")
        
        logger.info(f"User {user.id} has_phone: {has_phone}")
        
        if has_phone:
            # User already exists with phone number - go directly to main menu
            await query.edit_message_text(
                "Спасибо! Ваши данные уже сохранены в нашей базе."
            )
            
            # Send main menu directly
            keyboard = [
                [InlineKeyboardButton("Полезные файлы", callback_data="useful_files")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text="приветственное сообщение",
                reply_markup=reply_markup
            )
        else:
            # New user or user without phone - request contact information
            await query.edit_message_text(
                "Спасибо! Теперь нажмите кнопку 'Поделиться контактом' для предоставления ваших данных:"
            )
            
            # Then send a new message with the contact keyboard
            keyboard = [
                [KeyboardButton("📱 Поделиться контактом", request_contact=True)]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text="Нажмите кнопку ниже:",
                reply_markup=reply_markup
            )
    
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
    

    
    async def handle_phone_shared(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle when user shares their contact (includes all data)"""
        if update.message.contact:
            user = update.message.from_user
            contact = update.message.contact
            phone = contact.phone_number
            name = contact.first_name or contact.full_name or "Не указано"
            
            # Collect all user data at once
            user_data = {
                "telegram_id": user.id,
                "name": name,
                "username": user.username,
                "phone": phone
            }
            
            # Save all data to JSON
            if self.data_manager.save_user_data(user.id, user_data):
                # Remove the contact sharing keyboard by sending a message with remove_keyboard
                from telegram import ReplyKeyboardRemove
                await update.message.reply_text(
                    f"Спасибо! Ваши данные:\n"
                    f"Имя: {name}\n"
                    f"Телефон: {phone}\n"
                    f"Username: {user.username}\n\n"
                    f"Данные успешно сохранены. Мы свяжемся с вами в ближайшее время!",
                    reply_markup=ReplyKeyboardRemove()
                )
                
                # Send main menu directly
                keyboard = [
                    [InlineKeyboardButton("Полезные файлы", callback_data="useful_files")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text="приветственное сообщение",
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text("❌ Ошибка сохранения данных. Попробуйте позже.")
    

    

    
<<<<<<< HEAD
 
=======
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
>>>>>>> 66a159f1d1fd67fd9a0bc573f269d1f9c70a8801
