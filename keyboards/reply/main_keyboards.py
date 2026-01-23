from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_key():
    button_find = KeyboardButton(text="🔍 Найти собеседника.")
    button_stop = KeyboardButton(text="⏹️ СТОП.")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_find, button_stop)
    return keyboard


