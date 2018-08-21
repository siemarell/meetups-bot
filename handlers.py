import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from models import User, GetUserAddressTask, TaskStatus, Task, TASK_TYPES
from db import Session
from menus import keyboard_menu_markup, create_tasks_menu, MenuCommands
from custom_filters import reply_to_forward
from config import ADMIN_CHAT_ID
from messages import *
from task_factory import TaskFactory, TaskCreationException


logger = logging.getLogger(__name__)


def start(bot, update):
    chat_id = update.message.chat_id
    session = Session()
    user: User = session.query(User).filter(User.chat_id == chat_id).one_or_none()
    if not user:
        logger.info(f'New user {chat_id}')
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
    task_name = update.callback_query.data
    if user.active_task:
        msg = ACTIVE_TASK_MSG % user.active_task.description
        update.effective_message.reply_text(msg)
    else:
        try:
            task = TaskFactory.create_task(task_name, user)
            user.add_task(task)
            task.send_description(bot)
            session.commit()
        except TaskCreationException as e:
            update.effective_message.reply_text(str(e))
            logger.error(e)
    session.close()


def tasks(bot, update):
    chat_id = update.message.chat_id
    session = Session()
    user: User = session.query(User).filter(User.chat_id == chat_id).one()
    active_task = user.active_task
    if active_task:
        active_task.send_description(bot)
    else:
        tasks_menu = create_tasks_menu(TaskFactory.available_tasks(user))
        update.message.reply_text("Select task:", reply_markup=tasks_menu)
    session.close()


def ask_us(bot, update):
    update.message.reply_text(ASK_US_MSG)


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


def photo(bot, update):
    chat_id = update.message.chat_id
    session = Session()
    user: User = session.query(User).filter(User.chat_id == chat_id).one()
    active_task = user.active_task
    if active_task and active_task.result == 'image':
        full_image = update.message.photo[-1]
        if active_task.verify(full_image):
            session.commit()
            update.message.reply_text(active_task.on_complete_msg)
        else:
            update.message.reply_text(BAD_IMAGE_MSG)
    session.close()


handlers = [
    CommandHandler('start', start, filters=Filters.private),                                # Start command
    CommandHandler(['help', 'info'], helper, filters=Filters.private),                      # Help/info command
    CallbackQueryHandler(task_menu_callback),                                               # Task menu callback
    MessageHandler(Filters.private & Filters.command, unknown),                             # Unknown command
    MessageHandler(Filters.private & Filters.text & Filters.regex(MenuCommands.TASKS.value), tasks),    # Tasks command
    MessageHandler(Filters.private & Filters.text & Filters.regex(MenuCommands.ASK_US.value), ask_us),  # Ask us command
    MessageHandler(Filters.private & Filters.photo, photo),                                 # User photos
    MessageHandler(Filters.private & Filters.text, message),                                # User text messages
    MessageHandler(Filters.chat(ADMIN_CHAT_ID) & reply_to_forward, admin_reply),            # Admin reply to forwarded
]
