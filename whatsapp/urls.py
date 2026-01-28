from django.urls import path
from .views import *

urlpatterns = [
    path("webhook/", WhatsAppWebhook.as_view()),
    path("converse/", ConverseAPIView.as_view()),
    path(
        "conversation/<uuid:id>/",
        ConversationStatusAPIView.as_view(),
        name="conversation-status"
    ),
    
    
    ]

