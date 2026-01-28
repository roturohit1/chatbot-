from channels.generic.websocket import AsyncWebsocketConsumer
import json
import requests
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        question = data["question"]

        await self.send_json({"status": "thinking"})



        # run blocking ollama in thread
        answer = await asyncio.to_thread(self.ask_ollama, question)

        await self.send_json({
            "status": "done",
            "answer": answer
        })

    def ask_ollama(self, prompt):
        r = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 150}
            }
        )
        return r.json()["response"]
