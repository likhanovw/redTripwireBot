# TripwireBot - Telegram Bot

A Telegram bot that sends PDF files based on user selections through interactive buttons.

## Features

- ✅ Interactive button-based menu
- ✅ PDF file sending functionality
- ✅ Command handling (/start, /help)
- ✅ Error handling and logging
- ✅ Modular code structure

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- A Telegram bot token (get from @BotFather)

### 2. Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration

1. Create a `.env` file in the project root:
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   ```

2. Replace `your_telegram_bot_token_here` with your actual bot token from @BotFather

### 4. Adding PDF Files

1. Create a `pdfs` directory in the project root (it will be created automatically)
2. Add your PDF files to the `pdfs` directory with these exact names:
   - `Unites_for_users_presentation.pdf`
   - `user_guide.pdf`
   - `setup_instructions.pdf`
3. Update the button mappings in `bot.py` if you want different file names

### 5. Running the Bot

```bash
python bot.py
```

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` command
3. Choose an option from the buttons
4. The bot will send the corresponding PDF file

## Project Structure

```
tripwireBot/
├── bot.py              # Main bot file with handlers
├── config.py           # Configuration and environment variables
├── pdf_handler.py      # PDF file handling utilities
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .env               # Environment variables (create this)
└── pdfs/              # Directory for PDF files (auto-created)
```

## Available Commands

- `/start` - Start the bot and show available options
- `/help` - Show help information

## Customization

### Adding New PDF Options

1. Add new buttons in `bot.py` in the `start_command` method
2. Add corresponding callback data handling in `button_callback` method
3. Add the PDF file to the `pdfs` directory

### Changing Bot Name

Update the `BOT_NAME` and `BOT_USERNAME` variables in `config.py`

## Troubleshooting

### Common Issues

1. **Bot token error**: Make sure your `.env` file contains the correct bot token
2. **PDF not found**: Ensure PDF files exist in the `pdfs` directory
3. **Import errors**: Run `pip install -r requirements.txt`

### Logs

The bot logs all activities. Check the console output for debugging information.

## Security Notes

- Never commit your `.env` file to version control
- Keep your bot token secure
- The bot only sends files from the `pdfs` directory

## License

This project is open source and available under the MIT License. 