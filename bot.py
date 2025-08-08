import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN
from handlers.extendedUseRequest import ExtendedUseRequestHandler
from handlers.calculation_handler import CalculationHandler
from handlers.strategic_handler import StrategicHandler
from handlers.materials_handler import MaterialsHandler
from handlers.data_collection_handler import DataCollectionHandler

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
        
        self.extended_use_handler = ExtendedUseRequestHandler(pdf_handler)
        self.calculation_handler = CalculationHandler(pdf_handler)
        self.strategic_handler = StrategicHandler(pdf_handler)
        self.materials_handler = MaterialsHandler(pdf_handler)
        self.data_collection_handler = DataCollectionHandler(data_manager)
        
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all command and callback handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # Callback query handler for button clicks
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Message handlers for data collection
        self.application.add_handler(MessageHandler(filters.CONTACT, self.handle_contact))
    
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
                [InlineKeyboardButton("Заявка на расчет", callback_data="calculation")],
                [InlineKeyboardButton("Заявка на стратегическую сессию", callback_data="strategic")],
                [InlineKeyboardButton("Полезные материалы", callback_data="materials")]
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
        
        # Extended Use Request Handler
        if query.data == "has_product":
            await self.extended_use_handler.handle_has_product(query, context)
        elif query.data == "no_product":
            await self.extended_use_handler.handle_no_product(query, context)
        elif query.data == "own_team":
            await self.extended_use_handler.handle_own_team(query, context)
        elif query.data == "outstaff":
            await self.extended_use_handler.handle_outstaff(query, context)
        elif query.data in ["outsource", "no_team"]:
            await self.extended_use_handler.handle_other_team_options(query, context)
        elif query.data == "back_to_has_product":
            await self.extended_use_handler.handle_back_to_has_product(query, context)
        elif query.data in ["audit_processes", "audit_product", "audit_outstaff_specialists"]:
            await self.extended_use_handler.handle_audit_options(query, context)
        elif query.data in ["fully_own", "own_plus_external", "custom_development", "buy_customize"]:
            await self.extended_use_handler.handle_no_product_options(query, context)
        elif query.data == "back_to_start":
            await self.extended_use_handler.handle_back_to_start(query, context)
        
        # Calculation Handler
        elif query.data == "calculation":
            await self.calculation_handler.handle_calculation_request(query, context)
        
        # Strategic Handler
        elif query.data == "strategic":
            await self.strategic_handler.handle_strategic_request(query, context)
        
        # Materials Handler
        elif query.data == "materials":
            await self.materials_handler.handle_materials_request(query, context)
        elif query.data == "materials_file_1":
            await self.materials_handler.handle_materials_file_1(query, context)
        elif query.data == "materials_file_2":
            await self.materials_handler.handle_materials_file_2(query, context)
        elif query.data == "materials_file_3":
            await self.materials_handler.handle_materials_file_3(query, context)
        
        # Data Collection Handler
        elif query.data == "consent_yes":
            await self.data_collection_handler.handle_consent_yes(query, context)
        elif query.data == "consent_no":
            await self.data_collection_handler.handle_consent_no(query, context)
        elif query.data == "request_contact":
            await self.data_collection_handler.request_contact(query, context)
        elif query.data == "show_my_data":
            await self.data_collection_handler.show_user_data(query, context)
    
    async def handle_contact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle when user shares contact"""
        await self.data_collection_handler.handle_phone_shared(update, context)
    

    
    def run(self):
        """Start the bot"""
        logger.info("Starting TripwireBot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = TripwireBot()
    bot.run() 