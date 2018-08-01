from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from models import User, GetUserAddressTask, TaskStatus, Task
from db import Session
from filters import menu_command_filter

HELP_MSG = """Placeholder help message"""
START_MSG = """Placeholder start message"""
UNKNOWN_CMD_MSG = """Placeholder unknown command message"""


def start(bot, update):
    chat_id = update.message.chat_id
    session = Session()
    user: User = session.query(User).filter(User.chat_id == chat_id).one_or_none()
    if not user:
        # Initialize user and add first task
        user = User(chat_id)
        first_task = GetUserAddressTask()
        user.add_task(first_task)
        session.add(user)
        session.commit()
    session.close()
    # Send start message
    custom_keyboard = [['Tasks\u00A0', 'Ask us\u00A0']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(START_MSG, reply_markup=reply_markup)


def helper(bot, update):
    update.message.reply_text(HELP_MSG)


def unknown(bot, update):
    update.message.reply_text(UNKNOWN_CMD_MSG)


def menu(bot, update):
    pass


def menu_cmd(bot, update):
    print(update)


def message(bot, update):
    chat_id = update.message.chat_id
    session = Session()
    user: User = session.query(User).filter(User.chat_id == chat_id).one()
    if not user.active_task or not user.active_task.verify(update.message.text):
        forward(update)
    session.close()


handlers = [
    CommandHandler('start', start),                                       # Start command
    CommandHandler(['help', 'info'], helper),                             # Help/info command
    # CommandHandler('menu', menu),                                         # Menu command
    # CallbackQueryHandler(print),                                          # Menu callback
    MessageHandler(Filters.command, unknown),                             # Unknown command
    MessageHandler(menu_command_filter, menu_cmd),                        # Messages from keyboard
    MessageHandler(Filters.text, message)                                 # Text messages
]


def forward(update):
    pass
