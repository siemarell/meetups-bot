from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from enum import Enum, auto


class ReplyKeyboardMenuCommands(Enum):
    TASKS = 'Tasks'
    ASK_US = 'Ask us'


reply_keyboard_menu_markup = ReplyKeyboardMarkup([[ReplyKeyboardMenuCommands.TASKS.value,
                                                   ReplyKeyboardMenuCommands.ASK_US.value]])

cancel_task_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Cancel task', callback_data='cancel')]])


def _build_menu(buttons,
                n_cols,
                header_buttons=None,
                footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def get_tasks_menu_markup(task_types):
    button_list = [InlineKeyboardButton(s, callback_data=s) for s in task_types]
    tasks_menu = InlineKeyboardMarkup(_build_menu(button_list, n_cols=1))
    return tasks_menu


