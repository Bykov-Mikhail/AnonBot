from loader import bot
from database.chat_base import is_user_in_chat, get_partner

@bot.message_handler(func=lambda message: True)
def forward_massage(message):
    user_id = message.from_user.id
    if message.text and message.text.startswith('/'):
        return

    if is_user_in_chat(user_id):
        partner = get_partner(user_id)
        if partner:
            bot.send_message(partner, message.text)

    else:
        bot.send_message(user_id, "Сначала найди собеседника")