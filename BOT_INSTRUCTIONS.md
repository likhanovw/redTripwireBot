# 🤖 TripwireBot - Complete Instructions

## 📋 Overview
TripwireBot is a Telegram bot that collects user data with consent and provides various services including PDF delivery and data management.

## 🏗️ Architecture

### **File Structure:**
```
tripwireBot/
├── bot.py                           # Main bot file
├── config.py                        # Configuration (BOT_TOKEN)
├── data_manager.py                  # User data management
├── pdf_handler.py                   # PDF file handling
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables (BOT_TOKEN)
├── .gitignore                      # Git ignore rules
├── user_data.json                  # User data storage (auto-generated)
├── handlers/
│   ├── __init__.py
│   ├── data_collection_handler.py  # Consent and data collection
│   ├── extendedUseRequest.py       # Audit functionality
│   ├── calculation_handler.py       # Calculation requests
│   ├── strategic_handler.py         # Strategic sessions
│   └── materials_handler.py         # Useful materials
└── pdfs/                           # PDF files directory
    ├── frst_file.pdf
    ├── audit_processes.pdf
    ├── audit_product.pdf
    └── audit_outstaff_specialists.pdf
```

## 🚀 Setup Instructions

### **1. Environment Setup:**
```bash
# Clone the repository
git clone https://github.com/likhanovw/redTripwireBot.git
cd tripwireBot

# Install dependencies
pip3 install -r requirements.txt

# Create .env file with your bot token
echo "BOT_TOKEN=your_bot_token_here" > .env
```

### **2. Required Files:**
- **`.env`** - Contains `BOT_TOKEN=your_telegram_bot_token`
- **`pdfs/`** directory with PDF files:
  - `frst_file.pdf`
  - `audit_processes.pdf`
  - `audit_product.pdf`
  - `audit_outstaff_specialists.pdf`

### **3. Start the Bot:**
```bash
python3 bot.py
```

## 📊 Data Collection Flow

### **First-Time Users:**
1. **User sends `/start`** → Bot checks if user exists in database
2. **If new user** → Shows consent request
3. **User clicks "✅ Согласен"** → Bot requests contact sharing
4. **User clicks "📱 Поделиться"** → Contact sharing request
5. **User shares contact** → Bot collects name AND phone from contact
6. **Data saved** → User data stored in `user_data.json`
7. **Main menu shown** → Access to all services

### **Returning Users:**
1. **User sends `/start`** → Bot checks database
2. **If user exists** → Shows main menu directly
3. **No consent request** → Direct access to services

### **Users Who Decline:**
1. **User clicks "❌ Не согласен"** → Shows decline message
2. **"🔄 Попробовать снова" button** → Can retry consent
3. **No access to services** → Cannot proceed without consent

## 🔒 Security Features

### **Data Protection:**
- ✅ **GDPR Compliance** - Consent tracking with timestamps
- ✅ **Secure Storage** - User data in `user_data.json`
- ✅ **Privacy Protection** - `user_data.json` in `.gitignore`
- ✅ **Automatic Reloading** - No unsafe admin commands

### **Automatic Data Management:**
- ✅ **File Monitoring** - Checks for `user_data.json` changes
- ✅ **Auto-Reload** - Updates data when file modified
- ✅ **Transparent Operation** - No user intervention needed
- ✅ **Secure by Design** - No public admin commands
- ✅ **Data Deletion Protection** - Redirects to consent if user data deleted

## 📱 Bot Commands

### **Available Commands:**
- **`/start`** - Start the bot and begin data collection flow
- **`/help`** - Show help information

### **Button Interactions:**
- **Consent Buttons** - "✅ Согласен" / "❌ Не согласен"
- **Contact Sharing** - "📱 Поделиться"
- **Retry Button** - "🔄 Попробовать снова"
- **Main Menu** - "Заявка на расчет", "Заявка на стратегическую сессию", "Полезные материалы"

## 📊 Data Structure

### **user_data.json Format:**
```json
{
  "5202466309": {
    "consent_given": true,
    "consent_date": "2025-08-08T17:16:10.678",
    "data": {
      "telegram_id": 5202466309,
      "name": "User Name",
      "username": "username",
      "phone": "+7 999 123-45-67",
      "last_updated": "2025-08-08T17:16:14.584"
    },
    "last_updated": "2025-08-08T17:16:14.584"
  }
}
```

### **Collected Data:**
- **Name** - From shared contact
- **Phone** - From shared contact
- **Telegram ID** - User's Telegram ID
- **Username** - User's Telegram username
- **Consent Date** - When user gave consent
- **Last Updated** - Last data modification

## 🛠️ Data Management

### **Manual Data Management:**
```bash
# Edit user_data.json directly
nano user_data.json

# Bot will automatically reload on next /start
```

### **Delete User Data:**
```python
# Use the delete_user.py script
python3 delete_user.py
```

### **View Statistics:**
- **Total Users** - Number of users in database
- **Consent Rate** - Percentage of users who gave consent
- **Active Users** - Users with complete data

## 📁 File Management

### **PDF Files:**
- **Location** - `pdfs/` directory
- **Required Files**:
  - `frst_file.pdf` - First materials file
  - `audit_processes.pdf` - Audit processes PDF
  - `audit_product.pdf` - Audit product PDF
  - `audit_outstaff_specialists.pdf` - Outstaff audit PDF

### **Configuration:**
- **`.env`** - Bot token and configuration
- **`config.py`** - Bot settings and validation
- **`requirements.txt`** - Python dependencies

## 🔧 Troubleshooting

### **Common Issues:**

1. **Bot not responding:**
   - Check if `BOT_TOKEN` is correct in `.env`
   - Verify bot is running: `python3 bot.py`
   - Check logs for errors

2. **PDF files not found:**
   - Ensure PDF files exist in `pdfs/` directory
   - Check file names match exactly
   - Verify file permissions

3. **Data not saving:**
   - Check `user_data.json` permissions
   - Verify disk space
   - Check logs for save errors

4. **Contact sharing not working:**
   - Ensure user has phone number in Telegram
   - Check if user has contact sharing enabled
   - Verify bot has contact permission

### **Logs:**
- **Data Manager** - User data operations
- **PDF Handler** - File sending operations
- **Main Bot** - General bot operations
- **HTTP Requests** - Telegram API interactions

## 📈 Features

### **Current Features:**
- ✅ **Consent-based data collection**
- ✅ **Contact sharing integration**
- ✅ **PDF file delivery**
- ✅ **Modular handler architecture**
- ✅ **Automatic data reloading**
- ✅ **GDPR compliance**
- ✅ **Secure data storage**

### **Future Features:**
- 🔄 **Calculation requests** - In development
- 🔄 **Strategic sessions** - In development
- 🔄 **Materials management** - In development

## 🚀 Deployment

### **Production Setup:**
1. **Server Requirements:**
   - Python 3.8+
   - pip3
   - git

2. **Environment:**
   - Create `.env` with bot token
   - Install dependencies
   - Add PDF files to `pdfs/` directory

3. **Running:**
   ```bash
   python3 bot.py
   ```

4. **Monitoring:**
   - Check logs for errors
   - Monitor `user_data.json` size
   - Verify PDF file access

## 📞 Support

### **For Issues:**
- Check logs for error messages
- Verify all required files exist
- Ensure bot token is valid
- Test with `/start` command

### **Data Management:**
- Edit `user_data.json` directly
- Bot will auto-reload on next interaction
- No restart required for data changes
- **Data Deletion Protection** - If user data is deleted while bot is running, user will be redirected to consent flow on next button click

---

**Version:** 1.0  
**Last Updated:** 2025-08-08  
**Security Level:** Production Ready ✅ 