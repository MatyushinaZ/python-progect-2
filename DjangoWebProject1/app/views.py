from django.conf import settings
import telebot
from django.core.exceptions import PermissionDenied
from app import keyboards, base
import time

TOKEN = settings.TELEGRAM_API_TOKEN
bot = telebot.AsyncTeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    if str(message.chat.id) in base.get_users():
        bot.send_message(message.chat.id, "*Рады снова вас видеть\!*", reply_markup=keyboards.keyboard(), parse_mode='MarkdownV2')
    else:
        base.add_user(message.chat.id)
        bot.send_message(message.chat.id, "*Добро пожаловать\!*", reply_markup=keyboards.keyboard(), parse_mode='MarkdownV2')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'Добавить словарь':
        msg = bot.send_message(call.from_user.id, 'Введите название словаря: ')
        bot.register_next_step_handler(call.message, add_dict)
    if call.data == 'Просмотреть словари':
        response = '_Ваши словари:_\n'
        for d in base.get_dicts(call.from_user.id):
            response += f'{d}\n'
        bot.send_message(call.from_user.id, response, parse_mode='MarkdownV2')
    if call.data == 'Добавить урок':
        msg = bot.send_message(call.from_user.id, 'Введите дату в формате чч.мм.гггг: ')
        bot.register_next_step_handler(call.message, add_date)
    if call.data == 'Просмотреть уроки':
        response = '_Ваши уроки:_\n*Дата* *Темы* *Сложность*\n'
        for d in base.get_lessons(call.from_user.id):
            d_join = ''
            for i in d:
                d_join += str(i).replace('\n','') + ' '
            response += f'{d_join[:-1]}\n'
        bot.send_message(call.from_user.id, response.replace('.','\.'), parse_mode='MarkdownV2')
    if call.data == 'Добавить материал':
        msg = bot.send_message(call.from_user.id, 'Введите название: ')
        bot.register_next_step_handler(call.message, add_name)
    if call.data == 'Просмотреть материалы':
        response = '_Ваши уроки:_\n*Дата* *Темы* *Сложность*\n'
        for d in base.get_materials(call.from_user.id):
            name = d[0].replace('.','\.')
            mark = d[2].replace('\n','')
            response += f'[{name}]({d[1]}) {mark}\n'
        bot.send_message(call.from_user.id, response.replace('.','\.'), parse_mode='MarkdownV2')
    if call.data == 'Добавить слово':
        msg = bot.send_message(call.from_user.id, 'Выберите словарь: ', reply_markup = keyboards.dict_keyboard(call.from_user.id))
        bot.register_next_step_handler(call.message, add_word_rus)
    if call.data == 'Перевод':
        msg = bot.send_message(call.from_user.id, 'Выберите направление перевода: ', reply_markup = keyboards.trans_keyboard())
        bot.register_next_step_handler(call.message, choose_dict)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

def add_dict(message):
    base.add_dict(message.chat.id, message.text)
    bot.send_message(message.from_user.id, 'Словарь успешно добавлен!')

def add_date(message):
    try:
        valid_date = time.strptime(message.text, '%d.%m.%Y')
    except ValueError:
        msg = bot.send_message(message.from_user.id, 'Некорректная дата')
        return 0
    with open("./data/cash.txt", "a", encoding="utf-8") as f:
        f.write(f'{message.text}\t')
    msg = bot.send_message(message.from_user.id, 'Введите тему: ')
    bot.register_next_step_handler(message, add_thems)

def add_thems(message):
    with open("./data/cash.txt", "a", encoding="utf-8") as f:
        f.write(f'{message.text}')
    msg = bot.send_message(message.from_user.id, 'Введите оценку сложности: ', reply_markup = keyboards.mark_keyboard())
    bot.register_next_step_handler(message, add_mark)

def add_mark(message):
    with open("./data/cash.txt", "r", encoding="utf-8") as f:
        base.add_lesson(message.from_user.id, *f.readline().split('\t'), message.text)
    with open("./data/cash.txt", "w", encoding="utf-8") as f:
        f.write('')
    msg = bot.send_message(message.from_user.id, 'Урок успешно добавлен!')

def add_name(message):
    with open("./data/cash.txt", "a", encoding="utf-8") as f:
        f.write(f'{message.text},')
    msg = bot.send_message(message.from_user.id, 'Введите ссылку: ')
    bot.register_next_step_handler(message, add_link)

def add_link(message):
    with open("./data/cash.txt", "a", encoding="utf-8") as f:
        f.write(f'{message.text}')
    msg = bot.send_message(message.from_user.id, 'Введите оценку: ', reply_markup =keyboards.mark_keyboard())
    bot.register_next_step_handler(message, add_mark_mat)

def add_mark_mat(message):
    with open("./data/cash.txt", "r", encoding="utf-8") as f:
        base.add_material(message.from_user.id, *f.readline().split(','), message.text)
    with open("./data/cash.txt", "w", encoding="utf-8") as f:
        f.write('')
    msg = bot.send_message(message.from_user.id, 'Материал успешно добавлен!')

def add_word_rus(message):
    with open("./data/cash.txt", "a", encoding="utf-8") as f:
        f.write(f'{message.text},')
    if message.text not in base.get_dicts(message.from_user.id):
        bot.send_message(message.from_user.id, 'Словарь не найден, попробуйте снова')
        with open("./data/cash.txt", "w", encoding="utf-8") as f:
            f.write('')
        return(0)
    msg = bot.send_message(message.from_user.id, 'Введите русское слово: ')
    bot.register_next_step_handler(message, add_translate)

def add_translate(message):
    with open("./data/cash.txt", "a", encoding="utf-8") as f:
        f.write(f'{message.text.lower()}')
    msg = bot.send_message(message.from_user.id, 'Введите перевод: ')
    bot.register_next_step_handler(message, add_word_final)

def add_word_final(message):
    with open("./data/cash.txt", "r", encoding="utf-8") as f:
        base.add_word(message.from_user.id, *f.readline().split(','), message.text.lower())
    with open("./data/cash.txt", "w", encoding="utf-8") as f:
        f.write('')
    msg = bot.send_message(message.from_user.id, 'Слово успешно добавлено!')    
    
def choose_dict(message):
    with open("./data/cash.txt", "a", encoding="utf-8") as f:
        if message.text == 'На русский':
            f.write('0,')
        else:
            f.write('1,')
    msg = bot.send_message(message.from_user.id, 'Выберете словарь: ', reply_markup = keyboards.dict_keyboard(message.from_user.id))
    bot.register_next_step_handler(message, translate)

def translate(message):
    with open("./data/cash.txt", "a", encoding="utf-8") as f:
         f.write(f'{message.text}')
    if message.text not in base.get_dicts(message.from_user.id):
        bot.send_message(message.from_user.id, 'Словарь не найден, попробуйте снова')
        with open("./data/cash.txt", "w", encoding="utf-8") as f:
            f.write('')
        return(0)
    msg = bot.send_message(message.from_user.id, 'Ввведите слово: ')
    bot.register_next_step_handler(message, add_translate_final)

def add_translate_final(message):
    with open("./data/cash.txt", "r", encoding="utf-8") as f:
        translation = base.get_translte_word(message.from_user.id, *f.readline().split(','), message.text.lower())
    with open("./data/cash.txt", "w", encoding="utf-8") as f:
        f.write('')
    msg = bot.send_message(message.from_user.id, translation)    

bot.polling()