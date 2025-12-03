from dotenv import load_dotenv, find_dotenv
import os

if not find_dotenv:
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("find", "Запустить поиск"),
    ("help", "Вывести справку")
)
