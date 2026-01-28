import requests
from django.conf import settings

SYSTEM_PROMPT = """
You are Niantra's WhatsApp assistant.
Only answer questions related to Niantra services.
If the question is unrelated, say you can only help with Niantra.
"""

def ask_ollama(user_message):
    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": f"{SYSTEM_PROMPT}\nUser: {user_message}\nAssistant:",
        "stream": False
    }

    response = requests.post(
        settings.OLLAMA_URL,
        json=payload,
        timeout = 60
    )

    return response.json().get("response", "Sorry, I cannot answer right now.")
