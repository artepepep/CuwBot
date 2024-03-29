import os
import sqlite3

import telebot
from dotenv import load_dotenv
from telebot import types

from utils import generate_keyboard_buttons, main_buttons, tables_creation, post_to_db

load_dotenv()
SECRET_ID = os.getenv('TELEGRAM_BOT_ID')


bot = telebot.TeleBot(SECRET_ID)


@bot.message_handler(commands=['start'])
def start(info):

    tables_creation()

    bot.send_message(info.chat.id, f'Привіт, {info.from_user.first_name} {info.from_user.last_name}', reply_markup=generate_keyboard_buttons(main_buttons))
    bot.register_next_step_handler(info, post_keybord_buttons)


def post_keybord_buttons(сallback):
    if сallback.text == 'Новий Пост✅':
        bot.send_message(сallback.chat.id, 'Яка назва буде у вашого поста❓')
        bot.register_next_step_handler(сallback, get_name_for_post)
    elif сallback.text == 'Мої пости🎒':
        bot.send_message(сallback.chat.id, 'Мої пости🎒')
        bot.register_next_step_handler(сallback, post_keybord_buttons)
    elif сallback.text == 'Мої чати💬':
        bot.send_message(сallback.chat.id, 'Мої чати💬')
        bot.register_next_step_handler(сallback, post_keybord_buttons)
    elif сallback.text == 'Мої кошти💼':
        bot.send_message(сallback.chat.id, 'Мої кошти💼')
        bot.register_next_step_handler(сallback, post_keybord_buttons)


# беру имя для поста
def get_name_for_post(message):

    def check_name_len():
        if len(message.text) >= 50:
            bot.send_message(message.chat.id, '🔴Будь ласка, введіть менше 50 символів🔴')
            bot.register_next_step_handler(message, check_name_len)
        else:
            post_name = message.text
            bot.send_message(message.chat.id, 'Зробіть опис поста')
            bot.register_next_step_handler(message, get_details_for_post, post_name)

    check_name_len()


# беру описание поста
def get_details_for_post(message, post_name):

    def check_det_len():
        if len(message.text) >= 255:
            bot.send_message(message.chat.id, '🔴Будь ласка, введіть менше 255 символів🔴')
            bot.register_next_step_handler(message, check_det_len)
        else:
            post_details = message.text
            bot.send_message(message.chat.id, 'Будь ласка, введіть ціну за пост(У форматі числа)💸')
            bot.register_next_step_handler(message, get_price_for_post, post_name, post_details)

    check_det_len()


# беру цену для поста
def get_price_for_post(message, post_name, post_details):

    def check_price():
        if message.text.isdigit():
            post_price = float(message.text)
            add_post_to_db(message, post_name, post_details, post_price)
        else:
            bot.send_message(message.chat.id, '🔴Будь ласка, введіть коректну ціну за пост (у форматі числа)🔴')
            bot.register_next_step_handler(message, get_price_for_post, post_name, post_details)

    check_price()


# добавляю пост в базу данных
def add_post_to_db(message, post_name, post_details, post_price):
    # Сохраняем информацию о посте в базу данных
    customer_id = message.from_user.id
    post_to_db(post_name, post_price, post_details, customer_id)
    bot.send_message(message.chat.id, f'Пост "{post_name}" з ціною {post_price} успішно створено!')
    bot.register_next_step_handler(message, post_keybord_buttons)


@bot.message_handler(commands=['help'])
def help(info):
    bot.send_message(info.chat.id, 'Some help')


bot.polling(none_stop=True)