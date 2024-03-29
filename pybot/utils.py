from telebot import types


def generate_keyboard_buttons(btns_dict):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    btns = list(btns_dict.keys())
    for i in range(0, len(btns), 2):
        if i + 1 < len(btns):
            keyboard.add(btns[i], btns[i+1])
        else:
            keyboard.add(btns[i])
    return keyboard


def get_post_info():
    pass
    