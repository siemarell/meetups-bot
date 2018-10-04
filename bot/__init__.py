import telegram
from telegram.utils.request import Request
from config import BOT_TOKEN
from .handlers import *

request = Request(8)
bot = telegram.Bot(token=BOT_TOKEN,request=request)
