from config import APP_WAVES_ADDRESS

# Replies (handler file)
HELP_MSG = """Placeholder help message"""
START_MSG = """Placeholder start message"""
UNKNOWN_CMD_MSG = """Unknown command. Use /help or keyboard"""
ASK_US_MSG = """You can send your question to bot. Our admin will answer ASAP"""
ACTIVE_TASK_MSG = "You have an active task:\n%s"
ALREADY_COMPLETED_MSG = "Task \"%s\" has already been completed"
NOT_AVAILABLE_TASK_MSG = "Task %s is not available now"
BAD_IMAGE_MSG = """Image should contain exactly one face"""

# Task descriptions and onComplete messsages
# Get user address
GET_USER_ADDRESS_DESCRIPTION = f'Download Waves app and tell me your address'
GET_USER_ADDRESS_ON_COMPLETE_MSG = 'Congratulations! Now I have your address and you can choose next task'
# DEX Exchange
DEX_EXCHANGE_DESCRIPTION = 'Exchange WAVES to BTC using DEX'
DEX_EXCHANGE_ON_COMPLETE_MSG = 'Congratulations! DEX task completed'
# Send WAVES
SEND_WAVES_DESCRIPTION = f'Send 1 waves to {APP_WAVES_ADDRESS}'
SEND_WAVES_ON_COMPLETE_MSG = 'Completed send task'
# Send selfie
SEND_SELFIE_DESCRIPTION = 'Send me your selfie'
SEND_SELFIE_ON_COMPLETE_MSG = 'Congratulations! I\'ve got your picture'
# Find user
FIND_USER_DESCRIPTION = 'Find this user and, take his address and send it to me'
FIND_USER_ON_COMPLETE_MSG = 'Got it!'
