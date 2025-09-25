from django.urls import path

from ai.views.agent import AgentView

app_name = "ai"

urlpatterns = [
    path("chat/", AgentView.as_view(), name='chat')
]
