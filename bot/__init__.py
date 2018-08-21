import telegram
from config import BOT_TOKEN
from .handlers import *

bot = telegram.Bot(token=BOT_TOKEN)
