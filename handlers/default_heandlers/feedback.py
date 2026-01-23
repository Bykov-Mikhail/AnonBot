import smtplib
from email.mime.text import MIMEText
from config_data.config import SMTP_LOGIN, FEEDBACK_EMAIL, SMTP_PASSWORD
from loader import bot
from states.states import user_states

@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == "awaiting_feedback")
def handle_feedback(message):
    """
    Функция отвечает за взаимодействие пользователя с отзывом
    """
    user_id = message.from_user.id
    text = message.text

    try:
        msg = MIMEText(f"Отзыв от пользователя {user_id}:\n\n{text}", 'plain', 'utf-8')
        msg['Subject'] = "Отзыв от бота"
        msg['From'] = SMTP_LOGIN
        msg['To'] = FEEDBACK_EMAIL

        with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server:
            server.login(SMTP_LOGIN, SMTP_PASSWORD)
            server.sendmail(SMTP_LOGIN, FEEDBACK_EMAIL, msg.as_string())

        bot.send_message(user_id, "Спасибо за отзыв! 🙏 Он отправлен разработчику.")
    except Exception as e:
        bot.send_message(user_id, "Не удалось отправить отзыв.\n\n Да и забей тогда)\n\nСпасибо за попытку. До следующей встречи)")

    user_states.pop(user_id, None)