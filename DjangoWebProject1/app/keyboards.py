import telebot
from app import base

def menu_button(text):
    return telebot.types.InlineKeyboardButton(text, callback_data=text)

def keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(menu_button('Добавить словарь'), menu_button('Просмотреть словари'))
    keyboard.add(menu_button('Добавить урок'), menu_button('Просмотреть уроки'))
    keyboard.add(menu_button('Добавить материал'), menu_button('Просмотреть материалы'))
    keyboard.add(menu_button('Добавить слово'))
    keyboard.add(menu_button('Перевод'))
    return keyboard

def dict_keyboard(user):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    for d in base.get_dicts(user):
        keyboard.add(f'{d}')
    return keyboard

def mark_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    for m in range(1, 6):
        keyboard.add(f'{m}')
    keyboard.add(f'Без оценки')
    return keyboard

def trans_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('На русский')
    keyboard.row('С русского')
    return keyboard
    