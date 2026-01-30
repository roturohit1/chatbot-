from rest_framework import serializers
from .models import AIConversation

class AIConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIConversation
        fields = "__all__"
