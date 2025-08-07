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
        welcome_message = f"Hello {user.first_name}! 👋\n\nWelcome to TripwireBot! I'm here to help you with various resources."
        
        # Create inline keyboard with options
        keyboard = [
            [InlineKeyboardButton("📚 Documentation", callback_data="doc_pdf")],
            [InlineKeyboardButton("📖 User Guide", callback_data="guide_pdf")],
            [InlineKeyboardButton("🔧 Setup Instructions", callback_data="setup_pdf")],
            [InlineKeyboardButton("❓ Help", callback_data="help_info")]
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
        
        if query.data == "help_info":
            help_text = """
📋 **Available PDF Options:**

• **Documentation** - Complete technical documentation
• **User Guide** - Step-by-step user instructions  
• **Setup Instructions** - Installation and configuration guide

Click any button above to receive the corresponding PDF file.
            """
            await query.edit_message_text(help_text, parse_mode='Markdown')
            return
        
        # Handle PDF file requests
        pdf_files = {
            "doc_pdf": "Unites_for_users_presentation.pdf",
            "guide_pdf": "user_guide.pdf", 
            "setup_pdf": "setup_instructions.pdf"
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
                await query.edit_message_text("❌ Sorry, there was an error sending the PDF file.")
    
    def run(self):
        """Start the bot"""
        logger.info("Starting TripwireBot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = TripwireBot()
    bot.run() 