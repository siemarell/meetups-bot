from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from models import User, GetUserAddressTask, TaskStatus, Task, TASK_TYPES
from db import Session
from menus import keyboard_menu_markup, create_tasks_menu, MenuCommands
from custom_filters import reply_to_forward
from config import ADMIN_CHAT_ID

HELP_MSG = """Placeholder help message"""
START_MSG = """Placeholder start message"""
UNKNOWN_CMD_MSG = """Placeholder unknown command message"""
ASK_US_MESSAGE = """Placeholder ask us message"""


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
    update.message.reply_text(START_MSG, reply_markup=keyboard_menu_markup)


def helper(bot, update):
    update.message.reply_text(HELP_MSG)


def unknown(bot, update):
    update.message.reply_text(UNKNOWN_CMD_MSG)


def task_menu_callback(bot, update):
    chat_id = update.effective_user.id
    session = Session()
    user: User = session.query(User).filter(User.chat_id == chat_id).one()
    if user.active_task:
        msg = f"""You have an active task:\n{user.active_task.description}"""
        update.effective_message.reply_text(msg)
    else:
        task_name = update.callback_query.data
        task = next(filter(lambda x: x.name() == task_name, TASK_TYPES))()
        user.add_task(task)
        update.effective_message.reply_text(task.description)
        session.commit()
    session.close()


def tasks(bot, update):
    chat_id = update.message.chat_id
    session = Session()
    user: User = session.query(User).filter(User.chat_id == chat_id).one()
    if user.active_task:
        update.message.reply_text(user.active_task.description)
    else:
        tasks_menu = create_tasks_menu(user.available_tasks)
        update.message.reply_text("Select task:", reply_markup=tasks_menu)
    session.close()


def ask_us(bot, update):
    update.message.reply_text(ASK_US_MESSAGE)


def message(bot, update):
    chat_id = update.message.chat_id
    session = Session()
    user: User = session.query(User).filter(User.chat_id == chat_id).one()
    active_task = user.active_task
    if not active_task:
        forward_to_admin(bot, update)
    else:
        if active_task.result == 'message' and active_task.verify(update.message.text):
            session.commit()
            update.message.reply_text(active_task.on_complete_msg)
        else:
            forward_to_admin(bot, update)
    session.close()


def forward_to_admin(bot, update):
    bot.forwardMessage(ADMIN_CHAT_ID, update.message.chat_id, update.message.message_id)


def admin_reply(bot, update):
    bot.sendMessage(update.message.reply_to_message.forward_from.id, update.message.text)


handlers = [
    CommandHandler('start', start, filters=Filters.private),                                # Start command
    CommandHandler(['help', 'info'], helper, filters=Filters.private),                      # Help/info command
    # CommandHandler('menu', menu),                                                           # Menu command
    CallbackQueryHandler(task_menu_callback),                                               # Task menu callback
    MessageHandler(Filters.private & Filters.command, unknown),                             # Unknown command
    MessageHandler(Filters.private & Filters.regex(MenuCommands.TASKS.value), tasks),       # Tasks command
    MessageHandler(Filters.private & Filters.regex(MenuCommands.ASK_US.value), ask_us),     # Ask us command
    MessageHandler(Filters.private & Filters.text, message),                                # User text messages
    MessageHandler(Filters.chat(ADMIN_CHAT_ID) & reply_to_forward, admin_reply),            # Admin reply to forwarded
]