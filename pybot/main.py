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
btn7 = types.KeyboardButton('Мій рейтинг🌟')
btn8 = types.KeyboardButton('Список кидал🕵')

keyboard.add(btn1)
keyboard.add(btn2, btn3)
keyboard.add(btn4, btn5)
keyboard.add(btn6, btn7)
keyboard.add(btn8)


@bot.message_handler(commands=['start'])
def start(info):
    conn = sqlite3.connect('cuwbot.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    cur.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, publication_name VARCHAR(50), price DECIMAL(10,2), customer_id INTEGER, FOREIGN KEY (customer_id) REFERENCES users(id))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(info.chat.id, f'Привіт, {info.from_user.first_name} {info.from_user.last_name}', reply_markup=keyboard)
    bot.register_next_step_handler(info, post_keybord_buttons)

def post_keybord_buttons(сallback):
    if сallback.text == 'Стати виконавцем👩‍💻':
        bot.send_message(сallback.chat.id, 'Стати виконавцем')
    elif сallback.text == 'Новий Пост✅':
        bot.send_message(сallback.chat.id, 'Введіть назву посту')
        bot.register_next_step_handler(сallback, get_data_for_post)
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
    elif сallback.text == 'Список Порушників🕵':
        bot.send_message(сallback.chat.id, 'Список Порушників🕵')

def get_data_for_post(message):
    post_name = message.text
    bot.send_message(message.chat.id, 'Введіть ціну за пост або введіть exit щоб повернутись у головне меню')
    bot.register_next_step_handler(message, add_post_to_db, post_name)

def add_post_to_db(message, post_name):
    if message.text == 'exit':
        bot.register_next_step_handler(message, post_keybord_buttons)
    price = message.text
    if type(price) != int or float:
        bot.send_message(message.chat.id, 'Будь ласка, введіть коректну ціну за пост (у форматі числа) або введіть exit щоб повернутись у головне меню')
        bot.register_next_step_handler(message, get_data_for_post)
    price = float(message.text)
    # Сохраняем информацию о посте в базу данных
    conn = sqlite3.connect('cuwbot.sql')
    cur = conn.cursor()
    # Вставляем запись о посте в таблицу posts
    cur.execute("INSERT INTO posts (publication_name, price, customer_id) VALUES (?, ?, ?)", (post_name, price, message.from_user.id))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Пост "{post_name}" з ціною {price} успішно створено!')
    bot.register_next_step_handler(message, post_keybord_buttons)

@bot.message_handler(commands=['help'])
def help(info):
    bot.send_message(info.chat.id, 'Some help')


bot.polling(none_stop=True)