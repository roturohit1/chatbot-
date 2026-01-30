import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from .services.ai_engine import generate_ai_answer
from .services.memory import save_memory, fetch_memory
from .utils.helpers import clean_text

class AIConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope.get("user")
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        question = clean_text(data.get("question", ""))

        if not question:
            self.send(text_data=json.dumps({"error": "Empty question"}))
            return

        user = None if isinstance(self.user, AnonymousUser) else self.user
        memory = fetch_memory(user)

        answer = generate_ai_answer(question, memory)

        save_memory(user, question, answer)

        self.send(text_data=json.dumps({
            "question": question,
            "answer": answer
        })) 

