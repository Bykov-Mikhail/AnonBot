from loader import bot
from utils.gen_captcha import user_states
import sqlite3
from database.other_base import PATH_DB

@bot.message_handler(func=lambda msg: isinstance(user_states.get(msg.from_user.id), dict)
                        and user_states[msg.from_user.id].get("state") == "awaiting_answer_capcha")
def handle_captcha(message):
    """
    Функция отвечает за взаимодействие пользователя с капчей
    :param message:
    :return:
    """
    user_id = message.from_user.id
    user_answer = message.text
    state_data = user_states.get(user_id)

    if not state_data:
        return

    correct_answer = state_data['answer']
    attempts = state_data["attempts"]

    if user_answer != correct_answer and attempts != 10:
            new_attempts = attempts + 1
            first_num = state_data["first"]
            second_num = state_data["second"]
            user_states[user_id]["attempts"] = new_attempts

            bot.send_message(user_id, f"Ответ неверный, попробуй еще раз 😟\n\n"
                                      f"👹 Попытка № {new_attempts}\n\n"
                                      f"{first_num} + {second_num} =")
    elif user_answer != correct_answer and attempts == 10:
        with sqlite3.connect(PATH_DB, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ban_list (id) VALUES(?)", (user_id, ))
            user_states.pop(user_id, None)
            bot.send_message(user_id, "Ну все, ты в бане. 💀"
                                      "Для разбана пиши на эту почту diskoviya@mail.ru 🙉")
    else:
        bot.send_message(user_id, "Ты справился! 🤓")
        user_states.pop(user_id, None)
        return
