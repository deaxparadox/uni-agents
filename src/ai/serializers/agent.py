from adrf.serializers import Serializer
from rest_framework import serializers


class AgentSerializer(Serializer):
    user_input = serializers.CharField()