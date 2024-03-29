from telebot import types
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_name = os.getenv('DATABASE_NAME')
db_user = os.getenv('DATABASE_USERNAME')
db_password = os.getenv('DATABASE_PASSWORD')
db_host = os.getenv('DATABASE_HOST')
db_port = os.getenv('DATABASE_PORT')


# создаем клавиатурные кнопки
def generate_keyboard_buttons(btns_dict):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    btns = list(btns_dict.keys())
    for i in range(0, len(btns), 2):
        if i + 1 < len(btns):
            keyboard.add(btns[i], btns[i+1])
        else:
            keyboard.add(btns[i])
    return keyboard


# создание таблиц в базе данных
def tables_creation():
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                is_bad BOOLEAN,
                cash DECIMAL(10,2),
                tg_username VARCHAR(100)
                )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                publication_name VARCHAR(50),
                price DECIMAL(10,2),
                details VARCHAR(255),
                customer_id VARCHAR(100),
                status BOOLEAN
                )''')
    conn.commit()
    cur.close()
    conn.close()


# сохраняем пост в нашу таблицу posts
def post_to_db(post_name, post_price, post_details, customer_id):
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    cur = conn.cursor()
    # Вставляем запись о посте в таблицу posts
    cur.execute("INSERT INTO posts (publication_name, price, details, status, customer_id) VALUES (%s, %s, %s, %s, %s)", (post_name, post_price, post_details, False, customer_id))
    conn.commit()
    cur.close()
    conn.close()


def get_post_info():
    pass


main_buttons = {
    "Новий Пост✅": 'new_post',
    "Мої пости🎒": 'my_posts',
    "Мої чати💬": 'my_chats',
    "Мої кошти💼": 'my_cash'
}
