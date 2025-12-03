from loader import bot
from database.chat_base import remove_from_waiting, is_user_waiting, is_user_in_chat, disconnect_user, get_partner

@bot.message_handler(commands=["stop"])
def stop_function(message):
    user_id = message.chat.id
    if is_user_waiting(user_id):
        remove_from_waiting(user_id)
        bot.send_message(user_id, "Ты вышел из поиска")
    if is_user_in_chat(user_id):
        partner = get_partner(user_id)
        disconnect_user(user_id)
        bot.send_message(user_id, "Ты отключился от собеседника")
        bot.send_message(partner, "Собеседник отключился")

