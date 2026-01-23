import sqlite3
from pathlib import Path

current_dir = Path(__file__).parent
PATH_DB = current_dir / 'sqlite3' / 'database.db'

def add_to_waiting(user_id: int):
    """
    Функция добавляет пользователя в поиск
    :param user_id: переданный id
    :return: None
    """
    with sqlite3.connect(PATH_DB, check_same_thread=False) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO waiting_users (user_id) VALUES (?)", (user_id, ))
            conn.commit()
        except sqlite3.IntegrityError:
            pass

def remove_from_waiting(user_id: int):
    """
    Функция удаляет пользователя из поиска
    :param user_id: Переданный id
    :return: None
    """
    with sqlite3.connect(PATH_DB, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM waiting_users WHERE user_id = ?", (user_id, ))
        conn.commit()

def get_one_waiting_user(exclude_users_id: int = None) -> list[int] | None:
    """
    Функция подбирает человека из поиска исключая exclude_users_id(себя) и последних 3х пользователей
    :param exclude_users_id: Id пользователя
    :return:
    """
    past = get_past_partners(exclude_users_id)
    placeholders = ','.join('?' * len(past)) if past else 'NULL'
    with sqlite3.connect(PATH_DB, check_same_thread=False) as conn:
        cursor = conn.cursor()
        if past:
            cursor.execute(f"SELECT user_id FROM waiting_users WHERE user_id != ? AND user_id NOT IN ({placeholders}) LIMIT 1", (exclude_users_id, *past))
        else:
            cursor.execute("SELECT user_id FROM waiting_users WHERE user_id != ? LIMIT 1", (exclude_users_id, ))

        result = cursor.fetchone()
        return result[0] if result else None

def is_user_waiting(user_id: int) -> bool:
    """
    Функция проверяет в поиске ли пользователь
    :return:
    """
    with sqlite3.connect(PATH_DB, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM waiting_users WHERE user_id = ?", (user_id, ))
        result = cursor.fetchone() is not None
        return result

def is_user_in_chat(user_id: int) -> bool:
    """
    Функция проверяет в чате ли пользователь
    :param user_id:
    :return:
    """
    with sqlite3.connect(PATH_DB, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM connected_pairs WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        return result

def connect_pair(user1: int, user2: int):
    """
    Функция создает пары из пользователей в поиске и удаляет их из поиска
    user1, user2: user_id пользователя в поиске
    """
    with sqlite3.connect(PATH_DB, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO connected_pairs (user_id, partner_id) VALUES (?, ?)", (user1, user2))
        cursor.execute("INSERT INTO connected_pairs (user_id, partner_id) VALUES (?, ?)", (user2, user1))
        cursor.execute("DELETE FROM waiting_users WHERE user_id IN (?, ?)", (user1, user2))
        conn.commit()

def get_partner(user_id: int) -> int | None:
    """
    Функция выдает id собеседника
    :param user_id:
    :return:
    """
    with sqlite3.connect(PATH_DB, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT partner_id FROM connected_pairs WHERE user_id = ?", (user_id, ))
        result = cursor.fetchone()
        return result[0] if result else None

def disconnect_user(user_id: int):
    """
    Функция отключает пользователей друг от друга
    :param user_id:
    :return:
    """
    partner = get_partner(user_id)
    if partner is None:
        return
    with sqlite3.connect(PATH_DB, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM connected_pairs WHERE user_id = ? OR user_id = ?", (user_id, partner))
        conn.commit()
        return partner

def add_past_partners(user_id: int, partner_id: int):
    """
    Функция добавляет собеседников в таблицу прошлых собеседников
    :param user_id: id пользователя
    :param partner_id: id собеседника
    """
    with sqlite3.connect(PATH_DB, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM past_partners")
        list_partners = cursor.fetchall()
        if len(list_partners) >= 3:
            cursor.execute("DELETE FROM past_partners WHERE user_id = ? AND rowid = (SELECT rowid FROM past_partners WHERE user_id = ? ORDER BY rowid ASC LIMIT 1)",
                            (user_id, user_id))
            cursor.execute("INSERT INTO past_partners (user_id, partner_id) VALUES (?, ?)", (user_id, partner_id))
        else:
            cursor.execute("INSERT INTO past_partners (user_id, partner_id) VALUES (?, ?)", (user_id, partner_id))

def get_past_partners(user_id: int) -> list[int]:
    """
    Функция возвращает список прошлых собеседников
    :param user_id: id пользователя
    :return: список прошлых собеседников
    """
    with sqlite3.connect(PATH_DB, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT partner_id FROM past_partners WHERE user_id = ? ORDER BY rowid DESC LIMIT 3", (user_id, ))
        return [row[0] for row in cursor.fetchall()]














