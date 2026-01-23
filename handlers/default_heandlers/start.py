from loader import bot
from database.chat_base import is_user_waiting, is_user_in_chat
from keyboards.reply.main_keyboards import main_key

@bot.message_handler(commands=['start'])
def first_message(message):
    user_id = message.chat.id
    if not is_user_waiting(user_id) and not is_user_in_chat(user_id):
        bot.send_message(user_id, "👋 Привет!\n\n Я - 🤖 Anonimail, твой анонимный чат-бот. \n\nХочешь пообщаться с незнакомцем, который тоже ищет собеседника?\n\n"
                                  " Жми → /find и начнём! 🔍🥳\n\n", reply_markup=main_key())