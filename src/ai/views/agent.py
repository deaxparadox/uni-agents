from traceback import format_exc

from adrf.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ai.serializers.agent import AgentSerializer
from ai.agents.enterpreneur_agent import entrepreneur_agent

class AgentView(APIView):
    permission_classes = (IsAuthenticated, )
    
    async def post(self, request):
        try:
            chat_id = request.query_params.get("chat-id")
            agent_serializer = AgentSerializer(data=request.data)
            if agent_serializer.is_valid():
                user_input = agent_serializer.validated_data.get("user_input")
                response: str = await entrepreneur_agent(user_input, chat_id)
                return Response({"message": response}, status=status.HTTP_200_OK)   
            # if agent_serializer.is_valid():
            #     return Response({"message": "response"}, status=status.HTTP_200_OK)   
            return Response({"error": agent_serializer.errors}, status=status.HTTP_200_OK)
        except Exception as e:
            print(format_exc())
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)