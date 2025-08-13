# automation.py
import schedule
import time
import threading
from main import main  # reuse your main workflow

def algo_run():
    print(" Running Algo-Trading System...")
    main()
    print(" Algo run completed.\n")

def start_bot_listener():
    """
    Start bot listener for user collection in background
    """
    print(" Starting Bot Listener for user collection...")
    try:
        # Import bot listener functions
        import requests
        import json
        from datetime import datetime
        from config import TELEGRAM_BOT_TOKEN
        
        def get_telegram_updates(offset=None):
            """Get new messages from Telegram bot"""
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
            """Send welcome message to new user"""
            welcome_text = f"""
 Hello {first_name}!
 Welcome to our Market Information Bot!

ℹ<b>What I provide:</b>
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
            """Automatically collect user data and store in user_data.json"""
            try:
                # Extract user information
                chat = message.get('chat', {})
                chat_id = chat.get('id')
                username = chat.get('username', 'Unknown')
                first_name = chat.get('first_name', 'Unknown User')
                last_name = chat.get('last_name', '')
                full_name = f"{first_name} {last_name}".strip()
                
                print(f"\n🆕 NEW USER DETECTED:")
                print(f"👤 Name: {full_name}")
                print(f"📱 Username: @{username}")
                print(f"🆔 Chat ID: {chat_id}")
                
                # Load existing user data
                try:
                    with open('user_data.json', 'r') as f:
                        user_data = json.load(f)
                except:
                    user_data = {"registered_users": {}}
                
                chat_id_str = str(chat_id)
                
                # Check if user already exists
                if chat_id_str in user_data.get("registered_users", {}):
                    print(f" User {full_name} already registered")
                    send_welcome_message(chat_id, first_name)
                    return False
                
                # Add new user
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
                
                # Show updated count
                total_users = len(user_data["registered_users"])
                print(f" Total Users: {total_users}")      
                return True
                
            except Exception as e:
                print(f" Error processing user: {e}")
                return False

        # Main bot listener loop
        print(" Bot listener started - waiting for users...")
        last_update_id = 0
        
        while True:
            try:
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
                
            except Exception as e:
                print(f" Bot listener error: {e}")
                time.sleep(5)  # Wait 5 seconds on error
                
    except Exception as e:
        print(f" Failed to start bot listener: {e}")

def start_combined_system():
    """
    Start both trading system and bot listener
    """
    print(" STARTING COMPLETE ALGORITHMIC TRADING SYSTEM")
    print("=" * 60)
    
    # Start bot listener in background thread
    print(" Starting user collection system...")
    listener_thread = threading.Thread(target=start_bot_listener, daemon=True)
    listener_thread.start()
    
    # Wait a moment for bot listener to start
    time.sleep(2)
    
    # Run trading system immediately for testing
    print(" Running initial trading analysis...")
    algo_run()
    
    # Schedule trading system
    schedule.every(30).seconds.do(algo_run)  # Test every 30 seconds
    
    print("\n BOTH SYSTEMS ARE NOW RUNNING:")
    print(" Bot Listener: Collecting users continuously")
    print(" Trading System: Running every 30 seconds")
    print(" Press Ctrl+C to stop both systems")
    print(" Check users anytime: python view_users.py")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Shutting down all systems...")
        
        # Show final statistics
        try:
            import json
            with open('user_data.json', 'r') as f:
                data = json.load(f)
            total = len(data.get("registered_users", {}))
            print(f" Final Statistics: {total} users collected")
        except:
            pass
        print(" Goodbye!")

# For production daily runs (uncomment when ready)
def start_production_scheduler():
    """
    Production version - runs daily at market open
    """
    print(" STARTING PRODUCTION SYSTEM")
    print("=" * 40)
    
    # Start bot listener in background
    print("📱 Starting user collection system...")
    listener_thread = threading.Thread(target=start_bot_listener, daemon=True)
    listener_thread.start()
    
    # Schedule daily runs
    schedule.every().day.at("09:15").do(algo_run)
    
    print(" PRODUCTION SYSTEM READY:")
    print(" Bot Listener: Collecting users 24/7")
    print(" Trading System: Daily at 09:15 AM")
    print(" Waiting for next scheduled run...")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n Production system stopped")

# Choose which system to run
def start_scheduler():
    """
    Main function - choose between test and production
    """
    print(" ALGORITHMIC TRADING SYSTEM")
    print("=" * 40)
    
    # Uncomment the system you want:
    start_combined_system()      # Test system (30 seconds)
    # start_production_scheduler()  # Production system (daily)

if __name__ == "__main__":
    start_scheduler()