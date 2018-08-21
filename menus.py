from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from enum import Enum, auto


class MenuCommands(Enum):
    TASKS = 'Tasks'
    ASK_US = 'Ask us'


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


def create_tasks_menu(task_types):
    button_list = [InlineKeyboardButton(s, callback_data=s) for s in task_types]
    tasks_menu = InlineKeyboardMarkup(_build_menu(button_list, n_cols=1))
    return tasks_menu


keyboard_menu_markup = ReplyKeyboardMarkup([[MenuCommands.TASKS.value, MenuCommands.ASK_US.value]])

