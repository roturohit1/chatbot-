from django.db import models
import uuid 
from django.conf import settings
from django.utils import timezone
from .utils import * 




class ChatLog(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20)
    user_message = models.TextField()
    bot_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"ChatLog {self.id} - {self.phone}"
    

class Conversation(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    question = models.TextField()
    answer = models.TextField()
    time_taken_seconds = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30,choices=StatusEnum.choices(),default="processing")

    def __str__(self):
        return f"{self.user or 'Anonymous'} - {self.created_at}"
    
