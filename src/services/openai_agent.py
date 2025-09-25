from django.conf import settings
from langchain.chat_models import init_chat_model


openai_llm_chat = init_chat_model(f"openai:{settings.OPENAI_CHAT_MODEL}")