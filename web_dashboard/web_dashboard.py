from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

def load_user_data():
    """Load user data from JSON file"""
    try:
        with open('user_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading user data: {e}")
        return {}

def save_user_data(data):
    """Save user data to JSON file"""
    try:
        with open('user_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False

@app.route('/')
def dashboard():
    """Main dashboard page"""
    users = load_user_data()
    
    # Process users for display
    processed_users = []
    for user_id, user_data in users.items():
        if user_data.get("consent_given"):
            data = user_data.get("data", {})
            processed_users.append({
                "id": user_id,
                "name": data.get("name", "Не указано"),
                "username": data.get("username", "Не указано"),
                "phone": data.get("phone", "Не указан"),
                "contact_us": "✅" if user_data.get("contact_us") else "",
                "get_brief": "✅" if user_data.get("get_brief") else "",
                "consent_date": user_data.get("consent_date", "Не указана"),
                "last_updated": user_data.get("last_updated", "Не указана")
            })
    
    # Sort by last updated (newest first)
    processed_users.sort(key=lambda x: x["last_updated"], reverse=True)
    
    return render_template('dashboard.html', users=processed_users)

@app.route('/api/add_user', methods=['POST'])
def add_user():
    """API endpoint to add/update user data"""
    try:
        data = request.json
        user_id = str(data.get('user_id'))
        
        if not user_id:
            return jsonify({"status": "error", "message": "user_id is required"}), 400
        
        users = load_user_data()
        
        # Update or create user data
        if user_id not in users:
            users[user_id] = {
                "consent_given": True,
                "consent_date": datetime.now().isoformat(),
                "data": {},
                "contact_us": False,
                "get_brief": False,
                "last_updated": datetime.now().isoformat()
            }
        
        # Update user data
        if 'name' in data:
            users[user_id]["data"]["name"] = data['name']
        if 'username' in data:
            users[user_id]["data"]["username"] = data['username']
        if 'phone' in data:
            users[user_id]["data"]["phone"] = data['phone']
        if 'contact_us' in data:
            users[user_id]["contact_us"] = data['contact_us']
        if 'get_brief' in data:
            users[user_id]["get_brief"] = data['get_brief']
        
        users[user_id]["last_updated"] = datetime.now().isoformat()
        
        if save_user_data(users):
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Failed to save data"}), 500
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/users')
def get_users():
    """API endpoint to get all users"""
    users = load_user_data()
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 