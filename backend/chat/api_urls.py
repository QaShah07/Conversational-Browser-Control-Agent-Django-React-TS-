from django.urls import path
from .views import ConversationListCreate, MessageList

urlpatterns = [
    path('conversations/', ConversationListCreate.as_view()),
    path('conversations/<uuid:conv_id>/messages/', MessageList.as_view()),
]