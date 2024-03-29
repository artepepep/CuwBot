import telebot
from telebot import types
import sqlite3
import webbrowser
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_ID = os.getenv('TELEGRAM_BOT_ID')

bot = telebot.TeleBot(SECRET_ID)

keyboard = types.ReplyKeyboardMarkup(row_width=2)
btn1 = types.KeyboardButton('Стати виконавцем👩‍💻')
btn2 = types.KeyboardButton('Новий Пост✅')
btn3 = types.KeyboardButton('Нова Угода📄')
btn4 = types.KeyboardButton('Мої пости🎒')
btn5 = types.KeyboardButton('Мої чати💬')
btn6 = types.KeyboardButton('Мої кошти💼')

keyboard.add(btn1)
keyboard.add(btn2, btn3)
keyboard.add(btn4, btn5)
keyboard.add(btn6)

@bot.message_handler(commands=['start'])
def start(info):
    conn = sqlite3.connect('cuwbot.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, is_bad int)')
    cur.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, publication_name VARCHAR(50), price DECIMAL(10,2), details VARCHAR(255), customer_id INTEGER, FOREIGN KEY (customer_id) REFERENCES users(id))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(info.chat.id, f'Привіт, {info.from_user.first_name} {info.from_user.last_name}', reply_markup=keyboard)
    bot.register_next_step_handler(info, post_keybord_buttons)


def post_keybord_buttons(сallback):
    if сallback.text == 'Стати виконавцем👩‍💻':
        bot.send_message(сallback.chat.id, 'Стати виконавцем')
    elif сallback.text == 'Новий Пост✅':
        bot.send_message(сallback.chat.id, 'Яка назва буде у вашого поста❓')
        bot.register_next_step_handler(сallback, get_name_for_post)
    elif сallback.text == 'Нова Угода📄':
        bot.send_message(сallback.chat.id, 'Нова Угода📄')
    elif сallback.text == 'Мої пости🎒':
        bot.send_message(сallback.chat.id, 'Мої пости🎒')
    elif сallback.text == 'Мої чати💬':
        bot.send_message(сallback.chat.id, 'Мої чати💬')
    elif сallback.text == 'Мої кошти💼':
        bot.send_message(сallback.chat.id, 'Мої кошти💼')
    elif сallback.text == 'Мій рейтинг🌟':
        bot.send_message(сallback.chat.id, 'Мій рейтинг🌟')


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
    conn = sqlite3.connect('cuwbot.sql')
    cur = conn.cursor()
    # Вставляем запись о посте в таблицу posts
    cur.execute("INSERT INTO posts (publication_name, price, details, customer_id) VALUES (?, ?, ?, ?)", (post_name, post_price, post_details, message.from_user.id))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Пост "{post_name}" з ціною {post_price} успішно створено!')
    bot.register_next_step_handler(message, post_keybord_buttons)

@bot.message_handler(commands=['help'])
def help(info):
    bot.send_message(info.chat.id, 'Some help')

bot.polling(none_stop=True)