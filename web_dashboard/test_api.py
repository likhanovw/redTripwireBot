#!/usr/bin/env python3
"""
Test script for TripwireBot Web Dashboard API
Demonstrates how to send user data to the dashboard
"""

import requests
import json

def test_add_user():
    """Test adding a user to the dashboard"""
    
    # Test user data
    user_data = {
        "user_id": "123456789",
        "name": "Test User",
        "username": "testuser",
        "phone": "+1234567890",
        "contact_us": True,
        "get_brief": False
    }
    
    try:
        # Send data to the web dashboard
        response = requests.post(
            "http://localhost:5000/api/add_user",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Successfully added user to dashboard")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to dashboard. Make sure web_dashboard.py is running.")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_users():
    """Test getting all users from the dashboard"""
    
    try:
        response = requests.get("http://localhost:5000/api/users")
        
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Successfully retrieved {len(users)} users")
            print("Users:", json.dumps(users, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to dashboard. Make sure web_dashboard.py is running.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing TripwireBot Web Dashboard API")
    print("=" * 50)
    
    print("\n1. Testing add user...")
    test_add_user()
    
    print("\n2. Testing get users...")
    test_get_users()
    
    print("\n🌐 Dashboard URL: http://localhost:5000")
    print("📊 Open the URL in your browser to see the dashboard!") 