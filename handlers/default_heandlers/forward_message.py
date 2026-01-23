from loader import bot
from database.chat_base import is_user_in_chat, get_partner
from states.states import user_states

ALLOWED_CONTENT_TYPES = [
    'text', 'photo', 'document', 'audio', 'voice',
    'video', 'video_note', 'animation'
]

@bot.message_handler(content_types=ALLOWED_CONTENT_TYPES)
def forward_anonymous_message(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if message.content_type == 'text' and message.text and message.text.startswith('/'):
        return

    if isinstance(state, dict) and state.get("state") == "awaiting_answer_capcha":
        return
    if state == "awaiting_feedback":
        return

    if not is_user_in_chat(user_id):
        bot.send_message(user_id, "🥴 Сначала найди собеседника")
        return

    partner = get_partner(user_id)
    if not partner:
        bot.send_message(user_id, "🤔 Что-то пошло не так. Попробуй начать поиск заново.")
        return

    if message.content_type == 'text':
        bot.send_message(
            partner,
            message.text,
            entities=[],
            disable_web_page_preview=True
        )

    elif message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        bot.send_photo(partner, file_id, caption=message.caption)

    elif message.content_type == 'document':
        bot.send_document(partner, message.document.file_id, caption=message.caption)

    elif message.content_type == 'audio':
        bot.send_audio(partner, message.audio.file_id, caption=message.caption)

    elif message.content_type == 'voice':
        bot.send_voice(partner, message.voice.file_id)

    elif message.content_type == 'video':
        bot.send_video(partner, message.video.file_id, caption=message.caption)

    elif message.content_type == 'video_note':
        bot.send_video_note(partner, message.video_note.file_id)

    elif message.content_type == 'animation':
        bot.send_animation(partner, message.animation.file_id, caption=message.caption)