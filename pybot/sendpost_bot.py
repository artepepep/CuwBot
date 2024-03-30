import os
import time
import psycopg2

import telebot

from dotenv import load_dotenv

load_dotenv()
SECRET_POST_ID = os.getenv('TELEGRAM_POST_BOT_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')
bot = telebot.TeleBot(SECRET_POST_ID)

db_name = os.getenv('DATABASE_NAME')
db_user = os.getenv('DATABASE_USERNAME')
db_password = os.getenv('DATABASE_PASSWORD')
db_host = os.getenv('DATABASE_HOST')
db_port = os.getenv('DATABASE_PORT')

conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)
cur = conn.cursor()


def add_post_to_channel(post):
    message = f"Новый пост!\n\n{post[1]}\n\n{post[3]}\n\nЦена: {post[2]}\n\nАвтор: {post[5]}"
    bot.send_message(chat_id=CHANNEL_ID, text=message)
    print("sended")


def check_new_posts():
    cur.execute("SELECT * FROM posts WHERE posted = false")
    new_posts = cur.fetchall()
    for post in new_posts:
        add_post_to_channel(post)
        cur.execute("UPDATE posts SET posted = true WHERE id = %s", (post[0],))
        conn.commit()


while True:
    check_new_posts()
    time.sleep(3)