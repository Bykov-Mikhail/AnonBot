from dotenv import load_dotenv, find_dotenv
import os

if not find_dotenv:
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
FEEDBACK_EMAIL = os.getenv("FEEDBACK_EMAIL")
SMTP_LOGIN = os.getenv("SMTP_LOGIN")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("stop", "Выйти из чата/Выйти из поиска"),
    ("find", "Запустить поиск"),
    ("help", "Вывести справку")
)
