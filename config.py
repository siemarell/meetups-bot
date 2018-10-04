import os
import logging

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
ENV = os.environ.get('ENV', 'PROD')
# Background task check interval in seconds
CHECK_INTERVAL = int(os.environ.get('CHECK_INTERVAL')) if os.environ.get('CHECK_INTERVAL') else 5
REWARD_LIMIT = int(os.environ.get('REWARD_LIMIT')) if os.environ.get('REWARD_LIMIT') else 2
REWARD_VALUE = float(os.environ.get('REWARD_VALUE')) if os.environ.get('REWARD_VALUE') else 0.01
LOG_LEVEL = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG}[os.environ.get('LOG_LEVEL', 'INFO')]
LOG_PATH = os.environ.get('LOG_PATH') or 'logs'
