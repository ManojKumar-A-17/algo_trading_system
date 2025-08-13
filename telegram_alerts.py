# telegram_alerts.py

import requests
import time
import json
import os
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message_single(chat_id, message, max_retries=3):
    """
    Send a message to a single Telegram user with retry logic
    """
    for attempt in range(max_retries):
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                return True
            else:
                if attempt < max_retries - 1:
                    time.sleep(3)
                
        except requests.exceptions.ConnectTimeout:
            if attempt < max_retries - 1:
                time.sleep(5)
                
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(5)
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(3)
    
    return False

def load_user_data():
    """
    Load user data from JSON file
    """
    try:
        if os.path.exists('user_data.json'):
            with open('user_data.json', 'r') as f:
                return json.load(f)
    except:
        pass
    return {"registered_users": {}}

def save_user_data(data):
    """
    Save user data to JSON file
    """
    try:
        with open('user_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        return False

def get_chat_ids():
    """
    Get all registered chat IDs from user_data.json
    """
    try:
        user_data = load_user_data()
        registered_users = user_data.get("registered_users", {})
        chat_ids = [TELEGRAM_CHAT_ID]  # Always include original chat ID
        
        for chat_id in registered_users.keys():
            if chat_id not in chat_ids:
                chat_ids.append(chat_id)
        
        return chat_ids
    except:
        return [TELEGRAM_CHAT_ID]  # Fallback to original

def auto_add_user_silently(chat_id, username, first_name):
    """
    Silently add user to the system without them knowing
    """
    try:
        user_data = load_user_data()
        chat_id_str = str(chat_id)
        
        # Check if already registered
        if chat_id_str in user_data.get("registered_users", {}):
            return False  # Already exists
        
        # Add user silently
        if "registered_users" not in user_data:
            user_data["registered_users"] = {}
            
        user_data["registered_users"][chat_id_str] = {
            "name": first_name,
            "username": username or "Unknown",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "auto_added",
            "added_silently": True
        }
        
        save_user_data(user_data)
        
        # Silent log for admin (you can check user_data.json)
        print(f" Silently added user: {first_name} (ID: {chat_id})")
        return True
        
    except Exception as e:
        print(f" Error silently adding user: {e}")
        return False

def handle_new_user(chat_id, username, first_name):
    """
    Handle new user - silently add them and send innocent welcome message
    """
    # Silently add user to system
    auto_add_user_silently(chat_id, username, first_name)
    
    # Send innocent welcome message (they don't know they're added)
    welcome_message = f"""
 Hello {first_name}!
Welcome to our information bot!

ℹ<b>What I can help with:</b>
• General market information
• Financial news updates
• Economic insights
• Investment tips

 <b>Available Commands:</b>
/help - Show available commands
/info - Market information
/status - Bot status

Thank you for connecting! 
    """
    
    send_telegram_message_single(chat_id, welcome_message.strip())

def send_telegram_message_to_all(message, max_retries=3):
    """
    Send message to all users (including silently added ones)
    """
    chat_ids = get_chat_ids()
    success_count = 0
    
    for chat_id in chat_ids:
        if send_telegram_message_single(chat_id, message, max_retries):
            success_count += 1
    
    if success_count > 0:
        print(f" Alerts sent to {success_count}/{len(chat_ids)} users")
        return True
    else:
        print(f" Failed to send alerts")
        return False

def send_telegram_message(message, max_retries=3):
    """
    Enhanced main function - sends to all users (backward compatibility)
    """
    return send_telegram_message_to_all(message, max_retries)

def process_bot_command(chat_id, command, username, first_name):
    """
    Process commands - innocent responses to hide trading purpose
    """
    command = command.lower().strip()
    
    if command == "/start":
        handle_new_user(chat_id, username, first_name)
    
    elif command == "/help":
        help_message = """
 <b>Information Bot Commands</b>

/help - Show this help message
/info - General market information
/status - Bot operational status
/news - Latest financial updates

 <b>About:</b>
This bot provides general financial information and market insights for educational purposes.

 <b>Disclaimer:</b>
All information is for educational purposes only. Not financial advice.
        """
        send_telegram_message_single(chat_id, help_message.strip())
    
    elif command == "/info":
        info_message = """
 <b>Market Information</b>

 <b>Markets are complex systems influenced by:</b>
• Economic indicators
• Company performance
• Global events
• Investor sentiment

 <b>Key Investment Principles:</b>
• Diversification is important
• Long-term perspective matters
• Research before investing
• Risk management is crucial

 This is general educational information only.
        """
        send_telegram_message_single(chat_id, info_message.strip())
    
    elif command == "/status":
        send_telegram_message_single(chat_id, " Bot is operational and providing market information.")
    
    elif command == "/news":
        send_telegram_message_single(chat_id, " For latest financial news, check reputable financial news websites and official market sources.")
    
    else:
        send_telegram_message_single(chat_id, " Unknown command. Send /help for available commands.")

# Keep all existing functions but make them work with the silent user system
def send_trade_summary(symbol, total_trades, wins, win_rate, avg_pnl):
    """
    Send trading summary to all users (including silent ones)
    """
    try:
        message = f"""
 <b>Market Analysis Update - {symbol}</b>
 Analysis Points: {total_trades}
 Positive Signals: {wins}
 Success Rate: {win_rate:.2%}
 Average Movement: ₹{avg_pnl:.2f}

 <i>Educational market analysis for learning purposes</i>
        """
        send_telegram_message_to_all(message.strip())
    except Exception as e:
        print(f" Trade summary alert skipped: {e}")

def send_ml_accuracy(symbol, accuracy):
    """
    Send ML prediction accuracy (disguised as analysis)
    """
    try:
        message = f" <b>AI Market Analysis</b> - {symbol}: {accuracy:.2%} confidence level"
        send_telegram_message_to_all(message)
    except Exception as e:
        print(f" ML accuracy alert skipped: {e}")

def send_buy_signal_alert(symbol, date, price, rsi):
    """
    Send buy signal (disguised as market observation)
    """
    try:
        message = f"""
 <b>Market Observation Alert</b>
 Symbol: {symbol}
 Date: {date}
 Price Level: ₹{price:.2f}
 Technical Indicator: {rsi:.2f}
 Pattern: Oversold in uptrend detected
<i>Educational market pattern observation</i>
        """
        send_telegram_message_to_all(message.strip())
    except Exception as e:
        print(f"📱 Buy signal alert skipped: {e}")

def test_telegram_connection():
    """
    Test Telegram bot connection
    """
    print(" Testing Telegram connection...")
    test_message = " Information Bot Connection Test - System operational!"
    
    if send_telegram_message_to_all(test_message):
        print(" Telegram integration working perfectly!")
        return True
    else:
        print(" Telegram integration has issues but system will continue...")
        return False

def send_system_startup():
    """
    Send system startup notification (disguised)
    """
    try:
        message = """
 <b>Market Information System Started</b>
 System initialized successfully
 Monitoring: Indian stock markets
 Analysis: Technical indicators active
 Updates: Information service active
        """
        send_telegram_message_to_all(message.strip())
    except Exception as e:
        print(f"📱 Startup alert skipped: {e}")

def send_daily_summary(total_signals, total_trades, overall_accuracy):
    """
    Send daily system summary (disguised as market report)
    """
    try:
        message = f"""
 <b>Daily Market Analysis Report</b>
 Patterns Detected: {total_signals}
 Analysis Completed: {total_trades}
 System Accuracy: {overall_accuracy:.2%}
 Report Date: {time.strftime('%Y-%m-%d %H:%M:%S')}

 <i>Educational market analysis summary</i>
        """
        send_telegram_message_to_all(message.strip())
    except Exception as e:
        print(f"📱 Daily summary alert skipped: {e}")

# Secret admin function to see all users
def show_all_users():
    """
    Show all silently added users (for your eyes only)
    """
    try:
        user_data = load_user_data()
        users = user_data.get("registered_users", {})
        
        print("\n SECRET USER LIST:")
        print("=" * 40)
        for chat_id, info in users.items():
            print(f" {info['name']} (@{info.get('username', 'Unknown')})")
            print(f"ID: {chat_id}")
            print(f" Added: {info['timestamp']}")
            print(f" Silent: {info.get('added_silently', False)}")
            print("-" * 30)
        
        print(f" Total Users: {len(users)}")
        
    except Exception as e:
        print(f" Error showing users: {e}")

# Call this function when you want to see all silently added users
# show_all_users()