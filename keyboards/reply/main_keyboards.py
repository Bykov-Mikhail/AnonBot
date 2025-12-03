from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_key():
    button_find = KeyboardButton(text="/find")
    button_stop = KeyboardButton(text="/stop")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_find, button_stop)
    return keyboard


