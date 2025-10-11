from django.urls import path

from ai.views.agent import AgentView
from ai.views.chat_session import AgentChatIDView, AgentChatHistory
from ai.views.template import TemplateWorkbookView

app_name = "ai"

urlpatterns = [
    path("agent/", AgentView.as_view(), name='chat'),
    path("new-chat/", AgentChatIDView.as_view(), name="new-chat"),
    path("history/", AgentChatHistory.as_view(), name="chat-history"),
    path("template/<str:filename>/", TemplateWorkbookView.as_view(), name='template-workbook')
]
