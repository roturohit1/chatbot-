from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from rest_framework import status
from .services import send_whatsapp_message
from .models import *
from .bot import ask_ollama
from .serializers import *
from .tasks import *
from utils import *
import time
from django.utils import timezone




class WhatsAppWebhook(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.GET.get("hub.verify_token") == settings.WHATSAPP_VERIFY_TOKEN:
            return Response(request.GET.get("hub.challenge"))
        return Response(status=403)
    


    def post(self, request):
        try:
            msg = request.data["entry"][0]["changes"][0]["value"]["messages"][0]
            phone = msg["from"]
            text = msg["text"]["body"]
        except (KeyError, IndexError, TypeError):
            return Response("ok")

        serializer = ChatLogSerializer(data={
            "phone": phone,
            "user_message": text
        })
        serializer.is_valid(raise_exception=True)

        chat = serializer.save(bot_reply="")  # placeholder

        generate_whatsapp_reply.delay(chat.id)  # 🔥 async

        return Response("ok")

# class ConverseAPIView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         start_time = time.time()  # 👈 start timer

#         print("Converse API called")

#         serializer = ConversationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         question = serializer.validated_data["question"]
#         print("Question:", question)

#         convo = Conversation.objects.create(
#             user=request.user if request.user.is_authenticated else None,
#             question=question,
#             answer="",
#             time_taken_seconds=0
#         )

#         print("Conversation ID:", convo.id)

#         generate_conversation_reply.delay(convo.id)
#         print("Celery task sent")

#         duration = round(time.time() - start_time, 3)  
#         print(f"API response time: {duration} seconds")  

#         return Response(
#             {
#                 "id": convo.id,
#                 "status": "processing",
#                 "api_time_seconds": duration,       
#             },
#             status=status.HTTP_202_ACCEPTED
#         )



class ConverseAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        question = request.data.get("question")
        if not question:
            return Response({"error": "question required"}, status=400)

        convo = Conversation.objects.create(
            question=question,
            status="processing"
        )

        generate_conversation_reply.delay(convo.id)

        return Response({
            "id": str(convo.id),
            "status": "processing"
        }, status=202)
    
    
class ConversationStatusAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        convo = Conversation.objects.get(id=id)

        return Response({
            "status": convo.status,
            "answer": convo.answer
        })
