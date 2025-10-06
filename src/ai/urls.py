from django.urls import path

from ai.views.agent import AgentView
from ai.views.chat_session import AgentChatIDView

app_name = "ai"

urlpatterns = [
    path("agent/", AgentView.as_view(), name='chat'),
    path("new-chat/", AgentChatIDView.as_view(), name="new-chat")
]
