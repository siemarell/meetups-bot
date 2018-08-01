from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from enum import Enum, auto


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


class MenuCommands(Enum):
    TASKS = 'Tasks\u00A0'
    ASK_US = 'Ask us\u00A0'


button_list = [
    InlineKeyboardButton("col1", callback_data="asd"),
    InlineKeyboardButton("col2", callback_data="bcd"),
    InlineKeyboardButton("row 2", callback_data='cde')
]

tasks_menu = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
keyboard_menu_markup = ReplyKeyboardMarkup([[MenuCommands.TASKS.value, MenuCommands.ASK_US.value]])

