from traceback import format_exc

from adrf.views import APIView
from rest_framework import status
from rest_framework.response import Response

from ai.serializers.agent import AgentSerializer
from ai.agents.enterpreneur_agent import stream_graph_updates

class AgentView(APIView):
    async def post(self, request):
        try:
            agent_serializer = AgentSerializer(data=request.data)
            if agent_serializer.is_valid():
                await stream_graph_updates("What can you help me with?")
                return Response({"message": agent_serializer.data}, status=status.HTTP_200_OK)
            return Response({"error": agent_serializer.errros}, status=status.HTTP_200_OK)
        except Exception as e:
            print(format_exc())
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)