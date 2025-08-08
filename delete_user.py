#!/usr/bin/env python3
"""
Script to delete a specific user from data storage
"""

from data_manager import UserDataManager

def delete_user(user_id):
    """Delete user from data storage"""
    data_manager = UserDataManager()
    
    print(f"Attempting to delete user {user_id}...")
    
    if data_manager.delete_user_data(user_id):
        print(f"✅ User {user_id} successfully deleted!")
        
        # Show updated stats
        stats = data_manager.get_stats()
        print(f"📊 Updated stats:")
        print(f"   Total users: {stats['total_users']}")
        print(f"   Users with consent: {stats['users_with_consent']}")
        print(f"   Consent rate: {stats['consent_rate']:.1f}%")
    else:
        print(f"❌ User {user_id} not found in data storage")

if __name__ == "__main__":
    user_id = 5202466309
    delete_user(user_id) 