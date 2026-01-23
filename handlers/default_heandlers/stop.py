from loader import bot
from database.chat_base import remove_from_waiting, is_user_waiting, is_user_in_chat, disconnect_user, get_partner, add_past_partners
from database.other_base import add_quantity_chat
from utils.gen_captcha import user_states, generate_captcha_for_user

@bot.message_handler(func=lambda msg: (msg.text == "/stop" or msg.text == "⏹️ СТОП."))
def stop_function(message):
    user_id = message.chat.id

    if is_user_waiting(user_id):
        remove_from_waiting(user_id)
        bot.send_message(user_id, "Ты вышел из поиска 😰")

    if is_user_in_chat(user_id):
        partner = get_partner(user_id)
        disconnect_user(user_id)
        add_past_partners(user_id, partner)
        add_past_partners(partner, user_id)
        bot.send_message(user_id, "Ты отключился от собеседника 👌")
        bot.send_message(partner, "Собеседник отключился 😮‍💨")

        quantity = add_quantity_chat(user_id)
        quantity_partner = add_quantity_chat(partner)


        if quantity == 75:
            generate_captcha_for_user(user_id)
            first_num = user_states[user_id]["first"]
            second_num = user_states[user_id]["second"]

            bot.send_message(user_id, f"Придется решить капчу. 😬\n\n"
                                      f"Если не справишься за 10 попыток - бан (разбаниться будет не просто) ☣\n"
                                      f"✍️ Следующим сообщением отправь ответ на этот пример:\n\n"
                                      f"{first_num} + {second_num} =")


        if quantity_partner == 75:
            generate_captcha_for_user(user_id)
            first_num = user_states[partner]["first"]
            second_num = user_states[partner]["second"]

            bot.send_message(partner, f"Придется решить капчу. 😬\n"
                                      f"Если не справишься за 10 попыток - бан (разбаниться будет не просто) ☣\n"
                                      f"✍️ Следующим сообщением отправь ответ на этот пример:\n\n"
                                      f"{first_num} + {second_num} =")

        if quantity == 150:
            bot.send_message(user_id, "Привет! 👋\n\n"
                                      "Это разработчик этого бота. Следующее твоё сообщение улетит прямо мне в личку.\n\n"
                                      "Можешь, конечно, написать что угодно —\n"
                                      "но особенно круто будет, если поделишься идеями, как сделать бота лучше:\n"
                                      "что стоит добавить, улучшить или починить. 💡")
            user_states[user_id] = "awaiting_feedback"

        if quantity_partner == 150:
            bot.send_message(partner, "Привет! 👋\n\n"
                                      "Это разработчик этого бота. Следующее твоё сообщение улетит прямо мне в личку.\n\n"
                                      "Можешь, конечно, написать что угодно —\n"
                                      "но особенно круто будет, если поделишься идеями, как сделать бота лучше:\n"
                                      "что стоит добавить, улучшить или починить. 💡")
            user_states[user_id] = "awaiting_feedback"