# TripwireBot Web Dashboard

A simple web interface to view and manage user data from your Telegram bot.

## 🚀 Quick Start

### 1. Start the Dashboard
```bash
python3 web_dashboard.py
```

### 2. Open in Browser
Go to: http://localhost:5000

## 📊 Features

- **Real-time User Data** - Shows all users who gave consent
- **Statistics Cards** - Total users, contacted us, got brief, with phone
- **Interactive Table** - Sortable user data with all details
- **Auto-refresh** - Updates every 30 seconds
- **Modern UI** - Beautiful, responsive design

## 📋 Data Displayed

| Column | Description |
|--------|-------------|
| ID | Telegram User ID |
| Name | User's name |
| Username | Telegram username |
| Phone | User's phone number |
| Contact Us | ✅ if user clicked "Связаться" |
| Get Brief | ✅ if user downloaded brief |
| Consent Date | When user gave consent |
| Last Updated | Last activity timestamp |

## 🔌 API Endpoints

### Add/Update User
```bash
POST http://localhost:5000/api/add_user
Content-Type: application/json

{
    "user_id": "123456789",
    "name": "John Doe",
    "username": "johndoe",
    "phone": "+1234567890",
    "contact_us": true,
    "get_brief": false
}
```

### Get All Users
```bash
GET http://localhost:5000/api/users
```

## 🧪 Testing

Run the test script to verify everything works:
```bash
python3 test_api.py
```

## 📁 Files

- `web_dashboard.py` - Main Flask application
- `templates/dashboard.html` - Web interface template
- `test_api.py` - API testing script
- `user_data.json` - User data storage (auto-created)

## 🔧 Integration with Bot

The bot automatically tracks:
- ✅ **Contact Us** - When users click "Связаться"
- ✅ **Get Brief** - When users download the brief file
- ✅ **User Data** - Name, username, phone from consent

## 🌐 Access

- **Local:** http://localhost:5000
- **Network:** http://YOUR_IP:5000 (if needed)

## 🛠️ Customization

### Change Port
Edit `web_dashboard.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change port here
```

### Add More Statistics
Edit `templates/dashboard.html` and add new stat cards.

### Export Data
Add export functionality to download CSV/Excel files.

## 🔒 Security Notes

- Dashboard runs on localhost by default
- No authentication (add if needed for production)
- Uses existing `user_data.json` file
- No external dependencies or API keys needed

## 🚀 Production Deployment

For production use:
1. Add authentication
2. Use a proper WSGI server (gunicorn)
3. Set up HTTPS
4. Add rate limiting
5. Configure proper logging

---

**Simple, fast, and effective!** 🎯 