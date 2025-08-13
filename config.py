# config.py

STOCKS = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS']
DATA_PERIOD = '6mo'
DATA_INTERVAL = '1d'

# Telegram Configuration
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""  # Your original chat ID (admin)

# Silent User System Configuration
# Note: Additional users are automatically stored in user_data.json
# This file only contains your admin chat ID for security
# All silently added users are managed through the JSON file

# Bot Behavior Settings
BOT_NAME = "Market Info Bot"  # Innocent name for the bot
DISGUISE_MODE = True  # Hide trading purpose from users
AUTO_ADD_USERS = True  # Automatically add anyone who starts the bot
EDUCATIONAL_MODE = True  # Present alerts as educational content

# Admin Settings (only your chat ID has admin privileges)
ADMIN_CHAT_IDS = [
    "",  # Your chat ID (admin access)
]

# Trading Alert Settings
SEND_BUY_SIGNALS = True  # Send buy signal alerts
SEND_TRADE_SUMMARIES = True  # Send trading summaries
SEND_ML_ACCURACY = True  # Send ML accuracy updates
SEND_STARTUP_ALERTS = True  # Send system startup notifications
SEND_DAILY_SUMMARIES = True  # Send daily performance summaries

# Alert Timing (when to send different types of alerts)
ALERT_DELAY_SECONDS = 1  # Delay between sending alerts to multiple users
MAX_RETRIES = 3  # Maximum retries for failed message sends
TIMEOUT_SECONDS = 30  # Timeout for Telegram API calls

# File Paths for User Management
USER_DATA_FILE = "user_data.json"  # Where silent users are stored
USER_LOG_FILE = "user_activity.log"  # Optional: Log user interactions

# Security Settings
LOG_NEW_USERS = True  # Log when new users are added
NOTIFY_ADMIN_NEW_USERS = False  # Set to True if you want notifications for new users
BLOCK_SUSPICIOUS_USERS = False  # Advanced: Block users with suspicious behavior

# Message Customization
WELCOME_MESSAGE_STYLE = "educational"  # Style: educational, informational, casual
ALERT_MESSAGE_STYLE = "disguised"  # Style: disguised, direct, educational

# System Information
SYSTEM_VERSION = "2.0"
LAST_UPDATED = "2025-08-11"