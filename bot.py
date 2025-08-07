import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TripwireBot:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all command and callback handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # Callback query handler for button clicks
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_message = f"приветственное сообщение"
        
        # Create inline keyboard with options
        keyboard = [
            [InlineKeyboardButton("Есть продукт", callback_data="has_product")],
            [InlineKeyboardButton("Нет продукта", callback_data="no_product")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **TripwireBot Help**

**Available Commands:**
/start - Start the bot and see available options
/help - Show this help message

**How to use:**
1. Click "Start" to begin
2. Choose an option from the buttons
3. The bot will send you the requested PDF file

**Need more help?** Contact the bot administrator.
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()  # Answer the callback query
        
        if query.data == "has_product":
            # Create new keyboard for "Есть продукт" options
            keyboard = [
                [InlineKeyboardButton("Своя команда", callback_data="own_team")],
                [InlineKeyboardButton("Аутстафф", callback_data="outstaff")],
                [InlineKeyboardButton("Аутсорс", callback_data="outsource")],
                [InlineKeyboardButton("Нет никого", callback_data="no_team")],
                [InlineKeyboardButton("Назад", callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("✅ Есть продукт: выберите опцию", reply_markup=reply_markup)
            return
        elif query.data == "no_product":
            # Create new keyboard for "Нет продукта" options
            keyboard = [
                [InlineKeyboardButton("полностью сами", callback_data="fully_own")],
                [InlineKeyboardButton("Сами + усиление извне", callback_data="own_plus_external")],
                [InlineKeyboardButton("Заказная разработка", callback_data="custom_development")],
                [InlineKeyboardButton("Покупка готового продукта с кастомизацией", callback_data="buy_customize")],
                [InlineKeyboardButton("Назад", callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("❌ Нет продукта: выберите опцию", reply_markup=reply_markup)
            return
        elif query.data == "back_to_start":
            # Return to the main start menu
            keyboard = [
                [InlineKeyboardButton("Есть продукт", callback_data="has_product")],
                [InlineKeyboardButton("Нет продукта", callback_data="no_product")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("приветственное сообщение", reply_markup=reply_markup)
            return
        elif query.data == "own_team":
            # Create new keyboard for "own_team" options
            keyboard = [
                [InlineKeyboardButton("Аудит процессов + рекомендация проджекта", callback_data="audit_processes")],
                [InlineKeyboardButton("Аудит продукта + рекоммендации продакта", callback_data="audit_product")],
                [InlineKeyboardButton("Назад", callback_data="back_to_has_product")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("👥 Своя команда: выберите опцию", reply_markup=reply_markup)
            return
        elif query.data in ["outstaff", "outsource", "no_team"]:
            # Handle the other team options
            responses = {
                "outstaff": "👨‍💼 Аутстафф: выберите опцию",
                "outsource": "🏢 Аутсорс: выберите опцию",
                "no_team": "🚫 Нет никого: выберите опцию"
            }
            await query.edit_message_text(responses[query.data])
            return
        elif query.data == "back_to_has_product":
            # Return to the "Есть продукт" menu
            keyboard = [
                [InlineKeyboardButton("Своя команда", callback_data="own_team")],
                [InlineKeyboardButton("Аутстафф", callback_data="outstaff")],
                [InlineKeyboardButton("Аутсорс", callback_data="outsource")],
                [InlineKeyboardButton("Нет никого", callback_data="no_team")],
                [InlineKeyboardButton("Назад", callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("✅ Есть продукт: выберите опцию", reply_markup=reply_markup)
            return
        elif query.data in ["audit_processes", "audit_product"]:
            # Handle the audit options - send PDF files
            pdf_files = {
                "audit_processes": "audit_processes.pdf",
                "audit_product": "audit_product.pdf"
            }
            
            if query.data in pdf_files:
                filename = pdf_files[query.data]
                try:
                    # Import PDF handler and send the file
                    from pdf_handler import PDFHandler
                    pdf_handler = PDFHandler()
                    await pdf_handler.send_pdf(update, context, filename)
                except Exception as e:
                    logger.error(f"Error sending PDF {filename}: {e}")
                    await query.edit_message_text(f"❌ Ошибка отправки файла {filename}. Попробуйте позже.")
            return
        elif query.data in ["fully_own", "own_plus_external", "custom_development", "buy_customize"]:
            # Handle the no product options
            responses = {
                "fully_own": "🛠️ Полностью сами: выберите опцию",
                "own_plus_external": "🔧 Сами + усиление извне: выберите опцию",
                "custom_development": "📋 Заказная разработка: выберите опцию",
                "buy_customize": "🛒 Покупка готового продукта с кастомизацией: выберите опцию"
            }
            await query.edit_message_text(responses[query.data])
            return
    
    def run(self):
        """Start the bot"""
        logger.info("Starting TripwireBot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = TripwireBot()
    bot.run() 