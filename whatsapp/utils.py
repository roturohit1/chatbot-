import requests
import subprocess
from enum import Enum
class StatusEnum(Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    
    @classmethod 
    def choices(cls):
        return [(key.value, key.name) for key in cls]  

def ask_ollama(prompt: str) -> str:
    r = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "llama3:8b",   
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 150  
            }
        },
        timeout=120
    )
    return r.json()["response"]


def send_whatsapp_message(phone: str, text: str): 
    pass




