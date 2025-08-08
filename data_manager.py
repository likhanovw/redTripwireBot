import json
import os
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)

class UserDataManager:
    """Manages user data storage in JSON format"""
    
    def __init__(self, filename="user_data.json"):
        self.filename = filename
        self.last_modified_time = 0
        self.load_data()
    
    def load_data(self):
        """Load existing data from JSON file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                self.last_modified_time = os.path.getmtime(self.filename)
                logger.info(f"Loaded {len(self.data)} user records from {self.filename}")
            else:
                self.data = {}
                self.last_modified_time = 0
                logger.info(f"Created new data file: {self.filename}")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            self.data = {}
    
    def check_and_reload(self):
        """Check if file has been modified and reload if necessary"""
        try:
            if os.path.exists(self.filename):
                current_mtime = os.path.getmtime(self.filename)
                if current_mtime > self.last_modified_time:
                    with open(self.filename, 'r', encoding='utf-8') as f:
                        self.data = json.load(f)
                    self.last_modified_time = current_mtime
                    logger.info(f"Auto-reloaded {len(self.data)} user records from {self.filename}")
                    return True
        except Exception as e:
            logger.error(f"Error auto-reloading data: {e}")
        return False
    
    def reload_data(self):
        """Reload data from JSON file (useful when file is modified externally)"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                logger.info(f"Reloaded {len(self.data)} user records from {self.filename}")
                return True
            else:
                self.data = {}
                logger.info(f"Reloaded empty data file: {self.filename}")
                return True
        except Exception as e:
            logger.error(f"Error reloading data: {e}")
            return False
    
    def save_user_data(self, user_id, user_data):
        """Save user data with consent"""
        try:
            self.data[str(user_id)] = {
                "consent_given": True,
                "consent_date": datetime.now().isoformat(),
                "data": user_data,
                "last_updated": datetime.now().isoformat()
            }
            self.save_data()
            logger.info(f"Saved data for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving data for user {user_id}: {e}")
            return False
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data saved to {self.filename}")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def get_user_data(self, user_id):
        """Get user data by ID"""
        return self.data.get(str(user_id))
    
    def user_has_consent(self, user_id):
        """Check if user has given consent"""
        user_data = self.get_user_data(user_id)
        return user_data and user_data.get("consent_given", False)
    
    def delete_user_data(self, user_id):
        """Delete user data (GDPR compliance)"""
        if str(user_id) in self.data:
            del self.data[str(user_id)]
            self.save_data()
            logger.info(f"Deleted data for user {user_id}")
            return True
        return False
    
    def get_all_users(self):
        """Get all user IDs"""
        return list(self.data.keys())
    
    def get_stats(self):
        """Get data collection statistics"""
        total_users = len(self.data)
        users_with_consent = sum(1 for user in self.data.values() if user.get("consent_given", False))
        return {
            "total_users": total_users,
            "users_with_consent": users_with_consent,
            "consent_rate": (users_with_consent / total_users * 100) if total_users > 0 else 0
        } 