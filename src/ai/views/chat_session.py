from traceback import format_exc
from uuid import uuid4

from adrf.views import APIView
# from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ai.models import AgentChatIDModel
from services.langgraph.db import Saver
from utils.messsage import get_all_messages


class AgentChatIDView(APIView):
    permission_classes = (IsAuthenticated, )
    
    async def get(self, request):
        try:
            if request.user:
                chat_id = str(uuid4())
                cid = await AgentChatIDModel.objects.acreate(bubble_user=request.user, chat_id=chat_id)
                return Response(
                    {"message": {"chat_id": cid.chat_id, "chat_name": cid.chat_name}}, 
                    status=status.HTTP_201_CREATED
                )
            return Response({"error": "Invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(format_exc())
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class AgentChatHistory(APIView):
    permission_classes = (IsAuthenticated, )
    
    async def get(self, request):
        try:
            chat_id = request.query_params.get("chat-id")
            print("Chat id:", chat_id)
            chat_history = await Saver.saver.aget(config={"configurable": {"thread_id": chat_id}})
            print("chat_history:", chat_history)
            chat_history_structured = await get_all_messages(chat_history, ai_msg_json_format=True)
            print("chat_history_dict:", chat_history_structured)
            return Response({"message": chat_history_structured}, status=status.HTTP_200_OK)
        except Exception as e:
            print(format_exc())
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)