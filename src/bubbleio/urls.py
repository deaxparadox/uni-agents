from django.urls import path

from .views import BubbleDataView


app_name = "bubbleio"

urlpatterns = [
    path("auth/", BubbleDataView.as_view(), name="auth")
]
