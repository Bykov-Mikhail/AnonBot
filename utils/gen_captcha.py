from random import randint
from states.states import user_states

def generate_captcha_for_user(user_id: int):
    random_first_number = randint(1, 100)
    random_second_number = randint(1, 100)
    true_answer = random_first_number + random_second_number

    user_states[user_id] = {
        "state": "awaiting_answer_capcha",
        "first": random_first_number,
        "second": random_second_number,
        "answer": str(true_answer),
        "attempts": 1
    }