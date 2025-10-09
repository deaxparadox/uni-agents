from django.urls import re_path

from ai.consumers.agent_state import RouteTrackerConsumer

websocket_urlpatterns = [
    re_path(r'ws/route/(?P<session_id>[-\w]+)/$', RouteTrackerConsumer.as_asgi()),
]