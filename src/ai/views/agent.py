from adrf.views import APIView
from rest_framework import status
from rest_framework.response import Response

from ai.serializers.agent import AgentSerializer


class AgentView(APIView):
    async def post(self, request):
        try:
            agent_serializer = AgentSerializer(data=request.data)
            return Response({"message": agent_serializer}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)