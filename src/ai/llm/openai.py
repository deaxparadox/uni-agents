from django.conf import settings
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

from ai.tools.enterpreneur_search import get_bubble_entreprenurs, get_bubble_freelancers
from ai.prompts.entrepreneur_ideation_prompt import cofounder_ideation_agent_prompt


openai_llm_chat = init_chat_model(f"openai:{settings.OPENAI_CHAT_MODEL}")
ideation_llm_chat = create_react_agent(
    model=f"openai:{settings.OPENAI_CHAT_MODEL}",
    tools=[get_bubble_entreprenurs, get_bubble_freelancers],
    prompt=cofounder_ideation_agent_prompt
)