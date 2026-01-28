from rest_framework import serializers
from .models import *

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"
        read_only_fields = ("answer", "time_taken_seconds", "created_at", "user")



class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        fields = "__all__"
        read_only_fields = ("bot_reply", "created_at")        
