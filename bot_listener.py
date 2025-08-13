# bot_listener.py
import requests
import time
import json
from telegram_alerts import auto_add_user_silently, show_all_users
from config import TELEGRAM_BOT_TOKEN

def get_telegram_updates(offset=None):
    """
    Get new messages from Telegram bot
    """
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
        params = {'timeout': 10}
        if offset:
            params['offset'] = offset
            
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f" Error getting updates: {e}")
    return None

def send_welcome_message(chat_id, first_name):
    """
    Send welcome message to new user
    """
    welcome_text = f"""
 Hello {first_name}!
 Welcome to our Market Information Bot!

ℹ <b>What I provide:</b>
•  Market analysis and insights
•  Educational trading content
•  Investment learning materials
•  Financial news updates

 <b>Getting Started:</b>
You're all set! You'll receive helpful market information and educational content.

 <i>All information is for educational purposes only.</i>
    """
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': welcome_text.strip(),
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
    except:
        return False

def auto_collect_and_store_user(message):
    """
    Automatically collect user data and store in user_data.json
    """
    try:
        # Extract user information from message
        chat = message.get('chat', {})
        chat_id = chat.get('id')
        username = chat.get('username', 'Unknown')
        first_name = chat.get('first_name', 'Unknown User')
        last_name = chat.get('last_name', '')
        full_name = f"{first_name} {last_name}".strip()
        
        print(f"\n NEW USER DETECTED:")
        print(f" Name: {full_name}")
        print(f" Username: @{username}")
        print(f" Chat ID: {chat_id}")
        
        # Load existing user data
        try:
            with open('user_data.json', 'r') as f:
                user_data = json.load(f)
        except:
            user_data = {"registered_users": {}}
        
        chat_id_str = str(chat_id)
        
        # Check if user already exists
        if chat_id_str in user_data.get("registered_users", {}):
            print(f"ℹ User {full_name} already registered")
            send_welcome_message(chat_id, first_name)
            return False
        
        # Add new user to data
        from datetime import datetime
        user_data["registered_users"][chat_id_str] = {
            "name": full_name,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "chat_id": chat_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "auto_added",
            "added_silently": True,
            "source": "telegram_start"
        }
        
        # Save to user_data.json
        try:
            with open('user_data.json', 'w') as f:
                json.dump(user_data, f, indent=2)
            print(f" User {full_name} stored in user_data.json")
        except Exception as e:
            print(f" Error saving user data: {e}")
            return False
        
        # Send welcome message
        if send_welcome_message(chat_id, first_name):
            print(f" Welcome message sent to {full_name}")
        else:
            print(f" Failed to send welcome message")
        
        # Show updated user list
        print(f"\n UPDATED USER DATABASE:")
        total_users = len(user_data["registered_users"])
        print(f"Total Users: {total_users}")
        
        return True
        
    except Exception as e:
        print(f" Error processing user: {e}")
        return False

def start_bot_listener():
    """
    Start listening for new users
    """
    print(" Bot Listener Started!")
    print(" Waiting for users to click /start...")
    print(" Press Ctrl+C to stop\n")
    
    last_update_id = 0
    
    try:
        while True:
            updates = get_telegram_updates(last_update_id + 1)
            
            if updates and updates.get('ok'):
                for update in updates.get('result', []):
                    last_update_id = update.get('update_id', 0)
                    
                    message = update.get('message')
                    if message:
                        text = message.get('text', '').lower().strip()
                        
                        # Check if user clicked /start
                        if text == '/start':
                            auto_collect_and_store_user(message)
                        
                        # Handle other commands
                        elif text in ['/help', '/info']:
                            chat_id = message.get('chat', {}).get('id')
                            first_name = message.get('chat', {}).get('first_name', 'User')
                            send_welcome_message(chat_id, first_name)
            
            time.sleep(1)  # Check every second
            
    except KeyboardInterrupt:
        print("\n Bot Listener Stopped")
        
        # Show final user count
        try:
            with open('user_data.json', 'r') as f:
                user_data = json.load(f)
            total = len(user_data.get("registered_users", {}))
            print(f"📊 Final User Count: {total}")
        except:
            pass

if __name__ == "__main__":
    start_bot_listener()