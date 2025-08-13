import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN
# from handlers.extendedUseRequest import ExtendedUseRequestHandler
<<<<<<< HEAD
from handlers.calculation_handler import CalculationHandler
=======
# from handlers.calculation_handler import CalculationHandler
>>>>>>> 66a159f1d1fd67fd9a0bc573f269d1f9c70a8801
# from handlers.strategic_handler import StrategicHandler
# from handlers.materials_handler import MaterialsHandler
from handlers.data_collection_handler import DataCollectionHandler
from handlers.keyword_handler import KeywordHandler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TripwireBot:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Initialize handlers
<<<<<<< HEAD
        from pdf_handler import PDFHandler
        from data_manager import UserDataManager
        
        pdf_handler = PDFHandler()
        data_manager = UserDataManager()
        
        # self.extended_use_handler = ExtendedUseRequestHandler(pdf_handler)
        self.calculation_handler = CalculationHandler(pdf_handler)
=======
        # from pdf_handler import PDFHandler
        from data_manager import UserDataManager
        
        # pdf_handler = PDFHandler()
        data_manager = UserDataManager()
        
        # self.extended_use_handler = ExtendedUseRequestHandler(pdf_handler)
        # self.calculation_handler = CalculationHandler(pdf_handler)
>>>>>>> 66a159f1d1fd67fd9a0bc573f269d1f9c70a8801
        # self.strategic_handler = StrategicHandler(pdf_handler)
        # self.materials_handler = MaterialsHandler(pdf_handler)
        self.data_collection_handler = DataCollectionHandler(data_manager)
        self.keyword_handler = KeywordHandler()
        
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all command and callback handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("docs", self.docs_command))
        
        # Callback query handler for button clicks
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Message handlers for data collection
        self.application.add_handler(MessageHandler(filters.CONTACT, self.handle_contact))
        
        # Message handler for keyword detection
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        # Auto-reload data if file has been modified
        self.data_collection_handler.data_manager.check_and_reload()
        
        # Check if user has already given consent
        if self.data_collection_handler.data_manager.user_has_consent(user.id):
            # User already consented - show main menu
            welcome_message = f"приветственное сообщение"
            keyboard = [
                [InlineKeyboardButton("Полезные файлы", callback_data="useful_files")],
<<<<<<< HEAD
                [InlineKeyboardButton("Заявка на расчет", callback_data="calculation")],
=======
                # [InlineKeyboardButton("Заявка на расчет", callback_data="calculation")],
>>>>>>> 66a159f1d1fd67fd9a0bc573f269d1f9c70a8801
                # [InlineKeyboardButton("Заявка на стратегическую сессию", callback_data="strategic")],
                # [InlineKeyboardButton("Полезные материалы", callback_data="materials")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(welcome_message, reply_markup=reply_markup)
        else:
            # First time user - request consent
            await self.data_collection_handler.request_initial_consent(update, context)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **TripwireBot Help**

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

**Need more help?** Contact the bot administrator.
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def docs_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /docs command"""
        docs_message = "ссылки на доки"
        keyboard = [
            [InlineKeyboardButton("В начало", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(docs_message, reply_markup=reply_markup)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()  # Answer the callback query
        
        # Auto-reload data if file has been modified
        self.data_collection_handler.data_manager.check_and_reload()
        
        # Check if user has consent (except for consent-related buttons)
        consent_buttons = ["consent_yes", "consent_no"]
        if query.data not in consent_buttons:
            if not self.data_collection_handler.data_manager.user_has_consent(query.from_user.id):
                # User doesn't have consent - redirect to consent flow
                await self.data_collection_handler.request_consent(query, context)
                return
        
        # Useful Files Handler
        if query.data == "useful_files":
            await self.handle_useful_files(query, context)
        elif query.data == "back_to_start":
            # Go back to main menu
            await self.handle_back_to_start(query, context)
        elif query.data == "back_to_useful_files":
            # Go back to useful files menu
            await self.handle_useful_files(query, context)
        
        # Data Collection Handler
        elif query.data == "consent_yes":
            await self.data_collection_handler.handle_consent_yes(query, context)
        elif query.data == "consent_no":
            await self.data_collection_handler.handle_consent_no(query, context)
<<<<<<< HEAD

=======
        elif query.data == "show_my_data":
            await self.data_collection_handler.show_user_data(query, context)
>>>>>>> 66a159f1d1fd67fd9a0bc573f269d1f9c70a8801
        
        # Commented out old handlers for future use
        # # Extended Use Request Handler
        # elif query.data == "has_product":
        #     await self.extended_use_handler.handle_has_product(query, context)
        # elif query.data == "no_product":
        #     await self.extended_use_handler.handle_no_product(query, context)
        # elif query.data == "own_team":
        #     await self.extended_use_handler.handle_own_team(query, context)
        # elif query.data == "outstaff":
        #     await self.extended_use_handler.handle_outstaff(query, context)
        # elif query.data in ["outsource", "no_team"]:
        #     await self.extended_use_handler.handle_other_team_options(query, context)
        # elif query.data == "back_to_has_product":
        #     await self.extended_use_handler.handle_back_to_has_product(query, context)
        # elif query.data in ["audit_processes", "audit_product", "audit_outstaff_specialists"]:
        #     await self.extended_use_handler.handle_audit_options(query, context)
        # elif query.data in ["fully_own", "own_plus_external", "custom_development", "buy_customize"]:
        #     await self.extended_use_handler.handle_no_product_options(query, context)
        # elif query.data == "back_to_start":
        #     await self.extended_use_handler.handle_back_to_start(query, context)
        
<<<<<<< HEAD
        # Calculation Handler
        elif query.data == "calculation":
            await self.calculation_handler.handle_calculation_request(query, context)
        elif query.data == "get_brief":
            await self.handle_get_brief(query, context)
        elif query.data == "contact_us":
            await self.handle_contact_us(query, context)
=======
        # # Calculation Handler
        # elif query.data == "calculation":
        #     await self.calculation_handler.handle_calculation_request(query, context)
>>>>>>> 66a159f1d1fd67fd9a0bc573f269d1f9c70a8801
        
        # # Strategic Handler
        # elif query.data == "strategic":
        #     await self.strategic_handler.handle_strategic_request(query, context)
        
        # # Materials Handler
        # elif query.data == "materials":
        #     await self.materials_handler.handle_materials_request(query, context)
        # elif query.data == "materials_file_1":
        #     await self.materials_handler.handle_materials_file_1(query, context)
        # elif query.data == "materials_file_2":
        #     await self.materials_handler.handle_materials_file_2(query, context)
        # elif query.data == "materials_file_3":
        #     await self.materials_handler.handle_materials_file_3(query, context)
    
    async def handle_useful_files(self, query, context):
        """Handle useful files menu - show keyword instructions"""
        message_text = (
            "📁 Полезные файлы\n\n"
            "Чтобы получить нужный файл, отправьте мне сообщение с ключевым словом.\n\n"
            "**Доступные ключевые слова:**\n"
            "• аудит, процессы → audit_processes.pdf\n"
            "• продукт, продукта → audit_product.pdf\n"
            "• первый, файл → frst_file.pdf\n\n"
            "Просто напишите любое из этих слов, и я отправлю соответствующий PDF файл!"
        )
        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton("← В начало", callback_data="back_to_start")
        ]])
        
        # Check if the message has a document (PDF) - can't edit those
        if query.message.document:
            # PDF message - send new message instead of editing
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text=message_text,
                reply_markup=reply_markup
            )
        else:
            # Regular text message - edit existing message
            await query.edit_message_text(message_text, reply_markup=reply_markup)
    
    async def handle_back_to_start(self, query, context):
        """Handle back to start - show main menu"""
        user = query.from_user
        
        # Auto-reload data if file has been modified
        self.data_collection_handler.data_manager.check_and_reload()
        
        # Check if user has consent
        if not self.data_collection_handler.data_manager.user_has_consent(user.id):
            # User doesn't have consent - redirect to consent flow
            await self.data_collection_handler.request_consent(query, context)
            return
        
        # Show main menu
        welcome_message = f"приветственное сообщение"
        keyboard = [
            [InlineKeyboardButton("Полезные файлы", callback_data="useful_files")],
<<<<<<< HEAD
            [InlineKeyboardButton("Заявка на расчет", callback_data="calculation")],
=======
            # [InlineKeyboardButton("Заявка на расчет", callback_data="calculation")],
>>>>>>> 66a159f1d1fd67fd9a0bc573f269d1f9c70a8801
            # [InlineKeyboardButton("Заявка на стратегическую сессию", callback_data="strategic")],
            # [InlineKeyboardButton("Полезные материалы", callback_data="materials")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Check if the message has a document (PDF) - can't edit those
        if query.message.document:
            # PDF message - send new message instead of editing
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text=welcome_message,
                reply_markup=reply_markup
            )
        else:
            # Regular text message - edit existing message
            await query.edit_message_text(welcome_message, reply_markup=reply_markup)
    
    async def handle_contact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle when user shares contact"""
        await self.data_collection_handler.handle_phone_shared(update, context)
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages and check for keywords"""
        # Auto-reload data if file has been modified
        self.data_collection_handler.data_manager.check_and_reload()
        
        # Check if user has consent
        if not self.data_collection_handler.data_manager.user_has_consent(update.message.from_user.id):
            # User doesn't have consent - redirect to consent flow
            await self.data_collection_handler.request_consent(update, context)
            return
        
        # Check for keywords and send PDFs if found
        handled = await self.keyword_handler.handle_message(update, context)
        
        # If no keywords were found, you can add a default response here
        if not handled:
            # Optional: Send a helpful message when no keywords are found
            # await update.message.reply_text("Я не нашел ключевых слов в вашем сообщении. Попробуйте использовать слова: аудит, процессы, продукт, файл")
            pass
    
<<<<<<< HEAD
    async def handle_contact_us(self, query, context):
        """Handle contact us button from calculation handler"""
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("вот наши контакты напишите нам", reply_markup=reply_markup)
    
    async def handle_get_brief(self, query, context):
        """Handle get brief button from calculation handler"""
        try:
            # Send the RED.brief.odt file with back button attached
            keyboard = [
                [InlineKeyboardButton("Назад", callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            with open("RED.brief.odt", "rb") as file:
                await context.bot.send_document(
                    chat_id=query.from_user.id,
                    document=file,
                    filename="RED.brief.odt",
                    caption="📋 Бриф для расчета",
                    reply_markup=reply_markup
                )
            
        except FileNotFoundError:
            keyboard = [
                [InlineKeyboardButton("Назад", callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "❌ Файл бриф не найден. Обратитесь к администратору.",
                reply_markup=reply_markup
            )
        except Exception as e:
            keyboard = [
                [InlineKeyboardButton("Назад", callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"❌ Ошибка при отправке файла: {str(e)}",
                reply_markup=reply_markup
            )
    
=======
>>>>>>> 66a159f1d1fd67fd9a0bc573f269d1f9c70a8801
    def run(self):
        """Start the bot"""
        logger.info("Starting TripwireBot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = TripwireBot()
    bot.run() 