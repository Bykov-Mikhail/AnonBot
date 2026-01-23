import sqlite3
from pathlib import Path

current_dir = Path(__file__).parent
PATH_DB = current_dir / 'sqlite3' / 'database.db'

def add_quantity_chat(user_id: int) -> int:
    """
    Функция проверяет сколько чатов было у пользователя.
    Если чатов не было, то создает в базе user_id | 1
    Если чаты были, то добавляет +1: user_id | 1 (+1) = 2
    Если чатов 150, то скидывает до 1: user_id | 1
    :param user_id: id пользователя
    return кол-во чатов у пользователя
    """

    with sqlite3.connect(PATH_DB, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT quantity FROM quantity_chat WHERE user_id == ?", (user_id,))
        quantity = cursor.fetchone()
        if not quantity:
            cursor.execute("INSERT INTO quantity_chat (user_id, quantity) VALUES(?, ?)", (user_id, 1))
        elif quantity[0] > 150:
            cursor.execute("UPDATE quantity_chat SET quantity = 1 WHERE user_id == ?", (user_id, ))
        else:
            cursor.execute("UPDATE quantity_chat SET quantity = quantity + 1 WHERE user_id == ?", (user_id, ))

        cursor.execute("SELECT quantity FROM quantity_chat WHERE user_id == ?", (user_id,))
        quantity = cursor.fetchone()
        return quantity[0]

def get_banlist() -> list[int]:
    """
    Функция получает список всех пользователей из ban_list
    :return: список пользователей в бане
    """
    with sqlite3.connect(PATH_DB, check_same_thread= False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ban_list")
        all_id = [row[0] for row in cursor.fetchall()]
        return all_id