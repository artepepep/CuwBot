import telebot
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_ID = os.getenv('TELEGRAM_CHAT_BOT_ID')
# PAYMENT_ID = os.getenv('PORTMONE_PAY_ID')

chat_bot = telebot.TeleBot(SECRET_ID)