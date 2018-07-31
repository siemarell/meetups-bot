from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from models import User, GetUserAddressTask
from db import Session


def start(bot, update):
    session = Session()
    user = session.query(User).one_or_none()
    if not user:
        user = User(update.message.chat_id)
        first_task = GetUserAddressTask()
        user.add_task(first_task)
        update.message.reply_text(first_task.description)


def helper(bot, update):
    pass


def menu(bot, update):
    pass


def message(bot, update):
    pass


startHandler = CommandHandler('start', start)
helpHandler = CommandHandler('help', helper)
menuHandler = CommandHandler('menu', menu)
unknownCommandHandler = MessageHandler(Filters.command, helper)
messageHandler = MessageHandler(Filters.text, message)
