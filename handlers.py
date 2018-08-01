from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from models import User, GetUserAddressTask, TaskStatus, Task
from db import Session

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
    custom_keyboard = [['/tasks', 'ask us']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(START_MSG, reply_markup=reply_markup)


def helper(bot, update):
    update.message.reply_text(HELP_MSG)


def unknown(bot, update):
    update.message.reply_text(UNKNOWN_CMD_MSG)


def menu(bot, update):
    pass


def message(bot, update):
    chat_id = update.message.chat_id
    session = Session()
    user: User = session.query(User).filter(User.chat_id == chat_id).one()
    if not user.active_task or not user.active_task.verify(update.message.text):
        forward(update)
    session.close()


startHandler = CommandHandler('start', start)
helpHandler = CommandHandler(['help', 'info'], helper)
menuHandler = CommandHandler('menu', menu)
menuCallbackHandler = CallbackQueryHandler(print)
unknownCommandHandler = MessageHandler(Filters.command, unknown)
messageHandler = MessageHandler(Filters.text, message)


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def forward(update):
    pass