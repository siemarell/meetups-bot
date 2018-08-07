import os

# BLOCKCHAIN SETTINGS
CHAIN = os.environ.get('CHAIN') or 'testnet'
APP_ADDRESS = os.environ.get('REWARD_ADDRESS')
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')

# BOT SETTINGS
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_CHAT_ID = int(os.environ.get('ADMIN_CHAT_ID'))

# APP SETTINGS
CHECK_INTERVAL = os.environ.get('CHECK_INTERVAL') or 5  # Background task check interval in seconds
