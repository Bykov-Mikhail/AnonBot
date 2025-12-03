from loader import bot
from database.chat_base import add_to_waiting, remove_from_waiting, get_one_waiting_user, is_user_waiting, is_user_in_chat, connect_pair, get_partner, disconnect_user
from keyboards.reply.main_keyboards import main_key

@bot.message_handler(commands=['start'])
def first_message(message):
    user_id = message.chat.id
    if not is_user_waiting(user_id) and not is_user_in_chat(user_id):
        bot.send_message(user_id, "Привет, я бот Anonimail, если хочешь пообщаться с рандомными людьми, желающими того же, то ты попал по адресу\n"
                                  "Чтобы начать настройку твоего анонимного профиля напиши или жмакни /start (пока эта функция не работает, так что можешь сразу жмать, или написать /find\n"
                                  "Чтобы приступить к поиску собеседника, напиши или жмакни /find")

    bot.send_message(user_id,"Используй кнопки ниже для управления:", reply_markup=main_key())