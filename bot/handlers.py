import logging
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from models import User
from .menus import reply_keyboard_menu_markup, cancel_task_markup, get_tasks_menu_markup, ReplyKeyboardMenuCommands
from .custom_filters import reply_to_forward
from config import ADMIN_CHAT_ID
from .messages import *
from .utils import with_user
from task_factory import TaskFactory, TaskCreationException


logger = logging.getLogger(__name__)


@with_user
def start(bot, update, user):
    # We need to create new user if it doesnt exists. Thats why we use 'with_user' decorator
    update.message.reply_text(START_MSG, reply_markup=reply_keyboard_menu_markup)


def helper(bot, update):
    update.message.reply_text(HELP_MSG)


def unknown(bot, update):
    update.message.reply_text(UNKNOWN_CMD_MSG)


@with_user
def task_menu_callback(bot, update, user: User):
    task_name = update.callback_query.data
    if user.active_task:
        msg = ACTIVE_TASK_MSG % user.active_task.description
        update.effective_message.reply_text(msg)
    else:
        try:
            task = TaskFactory.create_task(task_name, user)
            user.add_task(task)
            task.send_description(bot)
        except TaskCreationException as e:
            update.effective_message.reply_text(str(e))
            logger.error(e)


@with_user
def task_cancel_callback(bot, update, user):
    active_task = user.active_task
    user.remove_task(active_task)
    bot.sendMessage(user.chat_id, TASK_REMOVED_MSG % active_task.name())


@with_user
def tasks(bot, update, user):
    active_task = user.active_task
    if active_task:
        active_task.send_description(bot)
        update.message.reply_text(CANCEL_MENU_TITLE, reply_markup=cancel_task_markup)
    else:
        tasks_menu = get_tasks_menu_markup(TaskFactory.available_tasks(user))
        update.message.reply_text(TASKS_MENU_TITLE, reply_markup=tasks_menu)


def ask_us(bot, update):
    update.message.reply_text(ASK_US_MSG)


@with_user
def message(bot, update, user):
    active_task = user.active_task
    if not active_task:
        forward_to_admin(bot, update)
    else:
        if active_task.result == 'message' and active_task.verify(update.message.text):
            update.message.reply_text(active_task.on_complete_msg)
        else:
            forward_to_admin(bot, update)


def forward_to_admin(bot, update):
    bot.forwardMessage(ADMIN_CHAT_ID, update.message.chat_id, update.message.message_id)


def admin_reply(bot, update):
    bot.sendMessage(update.message.reply_to_message.forward_from.id, update.message.text)


@with_user
def photo(bot, update, user):
    active_task = user.active_task
    if active_task and active_task.result == 'image':
        full_image = update.message.photo[-1]
        if active_task.verify(full_image):
            update.message.reply_text(active_task.on_complete_msg)
        else:
            update.message.reply_text(BAD_IMAGE_MSG)


handlers = [
    CommandHandler('start', start, filters=Filters.private),                                # Start command
    CommandHandler(['help', 'info'], helper, filters=Filters.private),                      # Help/info command
    CallbackQueryHandler(task_cancel_callback, pattern='cancel'),                           # Task menu callback
    CallbackQueryHandler(task_menu_callback),                                               # Task menu callback
    MessageHandler(Filters.private & Filters.command, unknown),                             # Unknown command
    MessageHandler(Filters.private & Filters.text &
                   Filters.regex(ReplyKeyboardMenuCommands.TASKS.value), tasks),            # Tasks command
    MessageHandler(Filters.private & Filters.text &
                   Filters.regex(ReplyKeyboardMenuCommands.ASK_US.value), ask_us),          # Ask us command
    MessageHandler(Filters.private & Filters.photo, photo),                                 # User photos
    MessageHandler(Filters.private & Filters.text, message),                                # User text messages
    MessageHandler(Filters.chat(ADMIN_CHAT_ID) & reply_to_forward, admin_reply),            # Admin reply to forwarded
]
