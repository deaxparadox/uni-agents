import json
from traceback import format_exc
from typing import Annotated

from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

from ai import graphs
from ai.prompts.entrepreneur_roadmap_prompt import (
    cofounder_agent_prompt,
    cofounder_agent_client_prompt
)


async def entrepreneur_agent(user_input: str, chat_id: str, /, system_prompt: str = cofounder_agent_client_prompt):

    message_state = {
        "messages": [
            # {"role": "system", "content": system_prompt}, 
            # {"role": "user", "content": user_input}
        ],
        "user_query": user_input,
        "chat_id": chat_id
    }
    
    
    response: str = ""
    async for chunk in graphs.entrepreneur_graph.astream(
        message_state,
        {"configurable": {"thread_id": chat_id}},
        stream_mode="updates"
    ):
        # response += chunk[0].content
        # for value in event.values():
        #     print(value)
            # print("Assistant:", value["messages"].content)
            
        if "entrepreneur_ideation_agent" in chunk:
            response = chunk["entrepreneur_ideation_agent"]['messages'][0]['content']
            
        if "entrepreneur_roadmap_agent" in chunk:
            response = chunk["entrepreneur_roadmap_agent"]['messages'][0]['content']
    try:
        # print(response)
        response = response.replace('```json', "").replace("```", "")
        # print("Stream Response:", {"response"})
        response = json.loads(response)
    except Exception as e:
        print(format_exc())
        pass
            
    return response