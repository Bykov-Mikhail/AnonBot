from loader import bot
from database.chat_base import add_to_waiting, get_one_waiting_user, is_user_waiting, is_user_in_chat, connect_pair, get_partner
from database.other_base import get_banlist
from keyboards.inline.sure_disconnect import sure_disconnect

@bot.message_handler(func=lambda msg: (msg.text == "/find" or msg.text == "🔍 Найти собеседника."))
def in_find(message):
    """
    Функция отвечает за поиск собеседника
    :param message: то что отправил пользователь боту
    """
    user_id = message.chat.id
    ban_list = get_banlist()

    if user_id in ban_list:
        bot.send_message(user_id, "Ты забанен!")
        return

    if is_user_in_chat(user_id):
        bot.send_message(user_id, "Ты уверен что хочешь найти нового собеседника? 🤔", reply_markup=sure_disconnect())
        return
    if is_user_waiting(user_id):
        bot.send_message(user_id, "Ты уже в поиске 🤨🤨")
        return
    else:
        add_to_waiting(user_id)
        bot.send_message(user_id, '🔍 Ищем собеседника...')

        partner = get_one_waiting_user(user_id)
        if partner is not None:
            connect_pair(user_id, partner)

        if is_user_in_chat(user_id):
            bot.send_message(user_id, "😱😱 Собеседник найден! Пиши скорее")
            bot.send_message(partner, "😱😱 Собеседник найден! Пиши скорее")
