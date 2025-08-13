import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, MESSAGES, BUTTONS, FILES
# from handlers.extendedUseRequest import ExtendedUseRequestHandler
from handlers.calculation_handler import CalculationHandler
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
        from pdf_handler import PDFHandler
        from data_manager import UserDataManager
        
        pdf_handler = PDFHandler()
        data_manager = UserDataManager()
        
        # self.extended_use_handler = ExtendedUseRequestHandler(pdf_handler)
        self.calculation_handler = CalculationHandler(pdf_handler)
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
            keyboard = [
                [InlineKeyboardButton(BUTTONS["useful_files"], callback_data="useful_files")],
                [InlineKeyboardButton(BUTTONS["calculation"], callback_data="calculation")],
                # [InlineKeyboardButton("Заявка на стратегическую сессию", callback_data="strategic")],
                # [InlineKeyboardButton("Полезные материалы", callback_data="materials")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(MESSAGES["welcome"], reply_markup=reply_markup)
        else:
            # First time user - request consent
            await self.data_collection_handler.request_initial_consent(update, context)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await update.message.reply_text(MESSAGES["help"], parse_mode='Markdown')
    
    async def docs_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /docs command"""
        keyboard = [
            [InlineKeyboardButton(BUTTONS["docs_back"], callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(MESSAGES["docs"], reply_markup=reply_markup)
    
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
        
        # Calculation Handler
        elif query.data == "calculation":
            await self.calculation_handler.handle_calculation_request(query, context)
        elif query.data == "get_brief":
            await self.handle_get_brief(query, context)
        elif query.data == "contact_us":
            await self.handle_contact_us(query, context)
    
    async def handle_useful_files(self, query, context):
        """Handle useful files menu - show keyword instructions"""
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(BUTTONS["back"], callback_data="back_to_start")]
        ])
        
        # Check if the message has a document (PDF) - can't edit those
        if query.message.document:
            # PDF message - send new message instead of editing
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text=MESSAGES["useful_files"],
                reply_markup=reply_markup
            )
        else:
            # Regular text message - edit existing message
            await query.edit_message_text(MESSAGES["useful_files"], reply_markup=reply_markup)
    
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
        keyboard = [
            [InlineKeyboardButton(BUTTONS["useful_files"], callback_data="useful_files")],
            [InlineKeyboardButton(BUTTONS["calculation"], callback_data="calculation")],
            # [InlineKeyboardButton("Заявка на стратегическую сессию", callback_data="strategic")],
            # [InlineKeyboardButton("Полезные материалы", callback_data="materials")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Check if the message has a document (PDF) - can't edit those
        if query.message.document:
            # PDF message - send new message instead of editing
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text=MESSAGES["welcome"],
                reply_markup=reply_markup
            )
        else:
            # Regular text message - edit existing message
            await query.edit_message_text(MESSAGES["welcome"], reply_markup=reply_markup)
    
    async def handle_contact_us(self, query, context):
        """Handle contact us button from calculation handler"""
        keyboard = [
            [InlineKeyboardButton(BUTTONS["back"], callback_data="calculation")],
            [InlineKeyboardButton(BUTTONS["main_menu"], callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(MESSAGES["contact_us"], reply_markup=reply_markup)
    
    async def handle_get_brief(self, query, context):
        """Handle get brief button from calculation handler"""
        try:
            # Send the RED.brief.odt file with navigation buttons attached (same as PDF files)
            keyboard = [
                [InlineKeyboardButton(BUTTONS["back"], callback_data="calculation")],
                [InlineKeyboardButton(BUTTONS["main_menu"], callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            with open(FILES["brief"], "rb") as file:
                await context.bot.send_document(
                    chat_id=query.from_user.id,
                    document=file,
                    filename=FILES["brief"],
                    caption=MESSAGES["brief_caption"],
                    reply_markup=reply_markup
                )
            
        except FileNotFoundError:
            keyboard = [
                [InlineKeyboardButton(BUTTONS["back"], callback_data="calculation")],
                [InlineKeyboardButton(BUTTONS["main_menu"], callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                MESSAGES["brief_not_found"],
                reply_markup=reply_markup
            )
        except Exception as e:
            keyboard = [
                [InlineKeyboardButton(BUTTONS["back"], callback_data="calculation")],
                [InlineKeyboardButton(BUTTONS["main_menu"], callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                MESSAGES["file_error"].format(str(e)),
                reply_markup=reply_markup
            )
    
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
    
    def run(self):
        """Start the bot"""
        logger.info("Starting TripwireBot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = TripwireBot()
    bot.run() 