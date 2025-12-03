from telebot.types import Message
from loader import bot
from config_data.config import DEFAULT_COMMANDS

@bot.message_handler(commands=["help"])
def send_helping(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
