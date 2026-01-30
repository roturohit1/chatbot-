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

    # def post(self, request):
    #     try:
    #         msg = request.data["entry"][0]["changes"][0]["value"]["messages"][0]
    #         phone = msg["from"]
    #         text = msg["text"]["body"]
    #     except (KeyError, IndexError, TypeError):
    #         return Response("ok")

    #     serializer = ChatLogSerializer(data={
    #         "phone": phone,
    #         "user_message": text
    #     })
    #     serializer.is_valid(raise_exception=True)

    #     reply = ask_ollama(text)

    #     chat = serializer.save(bot_reply=reply)

    #     send_whatsapp_message(phone, reply)
    #     return Response({"status": "sent"}, s tatus=status.HTTP_200_OK)
    



# class ConverseAPIView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         start_time = time.time()

#         serializer = ConversationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         question = serializer.validated_data["question"]

#         answer = ask_ollama(question)
#         duration = round(time.time() - start_time, 2)

#         convo = Conversation.objects.create(
#             user=request.user if request.user.is_authenticated else None,
#             question=question,
#             answer=answer,
#             time_taken_seconds=duration
#         )

#         return Response(
#             ConversationSerializer(convo).data,
#             status=status.HTTP_201_CREATED
# #         )
# class ConverseAPIView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = ConversationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         question = serializer.validated_data["question"]

#         convo = Conversation.objects.create(
#             user=request.user if request.user.is_authenticated else None,
#             question=question,
#             answer="",  
#             time_taken_seconds=0
#         )

#         generate_conversation_reply.delay(convo.id)  

#         return Response(
#             {"id": convo.id, "status": "processing"},
#             status=status.HTTP_202_ACCEPTED
#         )



class ConverseAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        start_time = time.time()  # 👈 start timer

        print("Converse API called")

        serializer = ConversationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data["question"]
        print("Question:", question)

        convo = Conversation.objects.create(
            user=request.user if request.user.is_authenticated else None,
            question=question,
            answer="",
            time_taken_seconds=0
        )

        print("Conversation ID:", convo.id)

        generate_conversation_reply.delay(convo.id)
        print("Celery task sent")

        duration = round(time.time() - start_time, 3)  
        print(f"API response time: {duration} seconds")  


        return Response(
            {
                "id": convo.id,
                "status": "processing",
                "api_time_seconds": duration,       
            },
            status=status.HTTP_202_ACCEPTED 
        )

class ConversationStatusAPIView(APIView):
    def get(self, request, id):
        convo = Conversation.objects.get(id=id)

        if convo.answer:
            return Response({
                "status": "completed",
                "answer": convo.answer,
                "time_taken_seconds": convo.time_taken_seconds
            })

        return Response({"status": "processing"})    
