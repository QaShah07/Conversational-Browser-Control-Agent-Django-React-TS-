from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from agent.tasks import process_user_message

class ConversationListCreate(APIView):
    def post(self, request):
        conv = Conversation.objects.create()
        return Response({'id': str(conv.id)}, status=201)

class MessageList(APIView):
    def get(self, request, conv_id):
        conv = get_object_or_404(Conversation, pk=conv_id)
        ser = ConversationSerializer(conv)
        return Response(ser.data)

    def post(self, request, conv_id):
        conv = get_object_or_404(Conversation, pk=conv_id)
        ser = MessageSerializer(data={**request.data, 'conversation': conv.id, 'role': 'user'})
        ser.is_valid(raise_exception=True)
        msg = ser.save()
        # enqueue agent pipeline
        process_user_message.send(str(msg.id))
        return Response(MessageSerializer(msg).data, status=201)