from celery import shared_task
from .models import *
from .utils import *
from django.utils import timezone



@shared_task
def generate_whatsapp_reply(chat_id):
    chat = ChatLog.objects.get(id=chat_id)
    reply = ask_ollama(chat.user_message)
    chat.bot_reply = reply
    chat.save(update_fields=["bot_reply"])
    send_whatsapp_message(chat.phone, reply)


@shared_task
def generate_conversation_reply(convo_id):
    convo = Conversation.objects.get(id=convo_id)

    start_time = convo.started_at  # 👈 start time from API

    answer = ask_ollama(convo.question)

    end_time = timezone.now()

    convo.answer = answer
    convo.time_taken_seconds = (end_time - start_time).total_seconds()
    convo.completed_at = end_time
    convo.save()

    print(
        f"Conversation {convo.id} completed in "
        f"{convo.time_taken_seconds:.2f} seconds"
    )