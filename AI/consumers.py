# ai/consumers.py
import json, requests
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class AIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        prompt = json.loads(text_data)["prompt"]

        response = await sync_to_async(requests.post)(
            "http://localhost:11434/api/generate",
            json={"model":"llama3","prompt":prompt,"stream":True},
            stream=True
        )

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode())
                if "response" in data:
                    await self.send(json.dumps({"token": data["response"]}))

        await self.send(json.dumps({"done": True}))
