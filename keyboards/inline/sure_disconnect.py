from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from database.chat_base import disconnect_user, get_partner, is_user_in_chat, is_user_waiting, add_to_waiting, get_one_waiting_user, connect_pair

def sure_disconnect():
    button_no = InlineKeyboardButton(text='Нет', callback_data='No')
    button_yes = InlineKeyboardButton(text="Уверен", callback_data='Sure')

    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_no, button_yes)
    return keyboard

@bot.callback_query_handler(func= lambda call : call.data in ['No', 'Sure'])
def handle_disconnect_confirmation(call):
    user_id = call.from_user.id
    partner = get_partner(user_id)
    if call.data == 'No':
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == 'Sure':
        disconnect_user(user_id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, "Ты отключился от собеседника")
        bot.send_message(partner, "Собеседник отключился")

    if is_user_in_chat(user_id):
        # Теоретически не должно быть, но на всякий случай
        bot.send_message(user_id, "Ошибка: всё ещё в чате.", reply_markup=sure_disconnect())
    elif is_user_waiting(user_id):
        bot.send_message(user_id, "Ты уже в поиске.")
    else:
        add_to_waiting(user_id)
        bot.send_message(user_id, "Ищем нового собеседника...")
        partner = get_one_waiting_user(user_id)
        if partner is not None:
            connect_pair(user_id, partner)
            bot.send_message(user_id, "Собеседник найден! Пиши скорее.")
            bot.send_message(partner, "Собеседник найден! Пиши скорее.")
