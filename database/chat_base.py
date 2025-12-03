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
    conn = sqlite3.connect(PATH_DB, check_same_thread=False, timeout=20)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO waiting_users (user_id) VALUES (?)", (user_id, ))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def remove_from_waiting(user_id: int):
    """
    Функция удаляет пользователя из поиска
    :param user_id: Переданный id
    :return: None
    """
    conn = sqlite3.connect(PATH_DB, check_same_thread=False, timeout=20)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM waiting_users WHERE user_id = ?", (user_id, ))
    conn.commit()
    conn.close()

def get_one_waiting_user(exclude_users_id: int = None):
    """
    Функция подбирает человека из поиска исключая exclude_users_id(себя)
    :param exclude_users_id:
    :return:
    """
    conn = sqlite3.connect(PATH_DB, check_same_thread=False, timeout=20)
    cursor = conn.cursor()
    if exclude_users_id is not None:
        cursor.execute("SELECT user_id FROM waiting_users WHERE user_id != ? LIMIT 1", (exclude_users_id, ))
    else:
        cursor.execute("SELECT user_id FROM waiting_users LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def is_user_waiting(user_id: int) -> bool:
    """
    Функция проверяет в поиске ли пользователь
    :return:
    """
    conn = sqlite3.connect(PATH_DB, check_same_thread=False, timeout=20)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM waiting_users WHERE user_id = ?", (user_id, ))
    result = cursor.fetchone() is not None
    conn.close()
    return result

def is_user_in_chat(user_id: int) -> bool:
    """
    Функция проверяет в чате ли пользователь
    :param user_id:
    :return:
    """
    conn = sqlite3.connect(PATH_DB, check_same_thread=False, timeout=20)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM connected_pairs WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def connect_pair(user1: int, user2: int):
    """
    Функция создает пары из пользователей в поиске и удаляет их из поиска
    user1, user2: user_id пользователя в поиске
    """
    conn = sqlite3.connect(PATH_DB, check_same_thread=False, timeout=20)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO connected_pairs (user_id, partner_id) VALUES (?, ?)", (user1, user2))
    cursor.execute("INSERT INTO connected_pairs (user_id, partner_id) VALUES (?, ?)", (user2, user1))
    cursor.execute("DELETE FROM waiting_users WHERE user_id IN (?, ?)", (user1, user2))
    conn.commit()
    conn.close()

def get_partner(user_id: int) -> int | None:
    """
    Функция выдает id собеседника
    :param user_id:
    :return:
    """
    conn = sqlite3.connect(PATH_DB, check_same_thread=False, timeout=20)
    cursor = conn.cursor()
    cursor.execute("SELECT partner_id FROM connected_pairs WHERE user_id = ?", (user_id, ))
    result = cursor.fetchone()
    conn.close()
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
    conn = sqlite3.connect(PATH_DB, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM connected_pairs WHERE user_id = ? OR user_id = ?", (user_id, partner))
    conn.commit()
    conn.close()
    return partner













