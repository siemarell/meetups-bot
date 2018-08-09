import os

# BLOCKCHAIN SETTINGS
CHAIN = os.environ.get('CHAIN') or 'testnet'
APP_WAVES_ADDRESS = os.environ.get('APP_WAVES_ADDRESS')
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')
NODES = {
    'testnet': 'https://testnodes.wavesnodes.com',
    'mainnet': 'https://nodes.wavesnodes.com'
}

# BOT SETTINGS
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_CHAT_ID = int(os.environ.get('ADMIN_CHAT_ID')) if os.environ.get('ADMIN_CHAT_ID') else None

# APP SETTINGS
# Background task check interval in seconds
ENV = os.environ.get('ENV', 'PROD')
CHECK_INTERVAL = int(os.environ.get('CHECK_INTERVAL')) if os.environ.get('CHECK_INTERVAL') else 5
