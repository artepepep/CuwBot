import os
import telebot
from dotenv import load_dotenv

from utils_profile import generate_keyboard_buttons, main_buttons, prices, tables_creation, post_to_db, get_my_posts

load_dotenv()
SECRET_ID = os.getenv('TELEGRAM_PROFILE_BOT_ID')
PAYMENT_TOKEN = os.getenv('PUBLIC_PAYMENT_TOKEN')
PAYMENT_TOKEN2 = os.getenv('PUBLIC_PAYMENT_TOKEN2')


bot = telebot.TeleBot(SECRET_ID)


@bot.message_handler(commands=['start'])
def start(info):

    tables_creation()

    bot.send_message(info.chat.id, f'Привіт, {info.from_user.first_name} {info.from_user.last_name}', reply_markup=generate_keyboard_buttons(main_buttons))
    bot.register_next_step_handler(info, post_keybord_buttons)


def post_keybord_buttons(сallback):
    if сallback.text == 'Новий Пост✅':
        bot.send_message(сallback.chat.id, 'Зробіть коротку назву завданню(до 50 символів)📍')
        bot.register_next_step_handler(сallback, get_name_for_post)
    elif сallback.text == 'Мої пости🎒':
        show_user_posts(сallback)
    elif сallback.text == 'Мої чати💬':
        bot.send_message(сallback.chat.id, 'Мої чати💬')
        bot.register_next_step_handler(сallback, post_keybord_buttons)
    elif сallback.text == 'Мої кошти💼':
        bot.send_message(сallback.chat.id, 'Мої кошти💼')
        bot.register_next_step_handler(сallback, post_keybord_buttons)
    elif сallback.text == 'Оплатити💲':
        pay_func(сallback)


# беру имя для поста
def get_name_for_post(message):

    def check_name_len(message):
        if len(message.text) >= 50:
            bot.send_message(message.chat.id, '🔴Будь ласка, введіть менше 50 символів🔴')
            bot.register_next_step_handler(message, check_name_len)
        else:
            post_name = message.text
            bot.send_message(message.chat.id, 'Напишіть подробиці (що б ви хотіли щоб викнавець зробив)📝')
            bot.register_next_step_handler(message, get_details_for_post, post_name)

    check_name_len(message)


# беру описание поста
def get_details_for_post(message, post_name):

    def check_det_len(message):
        if len(message.text) >= 1000:
            bot.send_message(message.chat.id, '🔴Будь ласка, введіть менше 1000 символів🔴')
            bot.register_next_step_handler(message, check_det_len)
        else:
            post_details = message.text
            bot.send_message(message.chat.id, 'Будь ласка, введіть ціну за пост(У форматі числа)💸')
            bot.register_next_step_handler(message, get_price_for_post, post_name, post_details)

    check_det_len(message)


# беру цену для поста
def get_price_for_post(message, post_name, post_details):

    def check_price(message):
        if message.text.isdigit():
            post_price = float(message.text)
            add_post_to_db(message, post_name, post_details, post_price)
        else:
            bot.send_message(message.chat.id, '🔴Будь ласка, введіть коректну ціну за пост (у форматі числа)🔴')
            bot.register_next_step_handler(message, get_price_for_post, post_name, post_details)

    check_price(message)


# добавляю пост в базу данных
def add_post_to_db(message, post_name, post_details, post_price):
    # Сохраняем информацию о посте в базу данных
    customer_id = message.from_user.id
    customer_username = message.from_user.username
    customer_fn = message.from_user.first_name
    post_to_db(post_name, post_price, post_details, customer_id, customer_username, customer_fn)
    bot.send_message(message.chat.id, f'Пост "{post_name}" з ціною {post_price} грн успішно створено!')
    bot.register_next_step_handler(message, post_keybord_buttons)


def show_user_posts(message):
    customer_id = message.from_user.id
    information = get_my_posts(customer_id)
    if information:
        post_number = 1
        for post in information:
            if not post[3]:
                user_link = f"<a href='tg://user?id={post[4]}'>{post[6]}</a>"
                post_str = f"\n\n🟢Пост #{post_number}"
                post_str += f"\n\n<b>{post[0]}</b>"
                post_str += f"\n\n{post[1]}"
                post_str += f"\n\nЦіна: {post[2]}"
                post_str += f"\n\nПисати {user_link}"
                bot.send_message(message.chat.id, post_str, parse_mode='HTML')
                post_number += 1
    else:
        bot.send_message(message.chat.id, "У вас немає постів🫤")
    bot.register_next_step_handler(message, post_keybord_buttons)


def pay_func(message):
    bot.send_invoice(
        message.chat.id,  #chat_id
        'Working Time Machine', #title
        ' Want to visit your great-great-great-grandparents? Make a fortune at the races? Shake hands with Hammurabi and take a stroll in the Hanging Gardens? Order our Working Time Machine today!', #description
        'HAPPY FRIDAYS COUPON', #invoice_payload
        PAYMENT_TOKEN2, #provider_token
        'usd', #currency
        prices, #prices
        photo_url='https://hips.hearstapps.com/hmg-prod/images/bmw-vision-neue-klasse-concept-car5-64ecd9b81229e.jpg?crop=1.00xw:0.753xh;0,0.166xh&resize=1200:*',
        is_flexible=False,  # True If you need to set up Shipping Fee
        start_parameter='time-machine-example')
    bot.register_next_step_handler(message, post_keybord_buttons)


@bot.message_handler(commands=['help'])
def help(info):
    bot.send_message(info.chat.id, 'Some help')


bot.polling(none_stop=True)