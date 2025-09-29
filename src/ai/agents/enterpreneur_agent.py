import json
from traceback import format_exc
from typing import Annotated

from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

from ai.prompts.enterpreneur_assistant import enterpreneur_agent_prompt
from ai.graphs import entrepreneur_graph

class State(TypedDict):
    messages: Annotated[list, add_messages]


async def entrepreneur_agent(user_input: str, system_prompt: str = enterpreneur_agent_prompt):

    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": user_input}
    ]
    
    response: str = ""
    async for chunk in entrepreneur_graph.astream(
        {"messages": messages},
        {"configurable": {"thread_id": "1"}},
        stream_mode="messages",
    ):
        response += chunk[0].content
        # for value in event.values():
        #     print(value)
            # print("Assistant:", value["messages"].content)
    try:
        print(response)
        response = response.replace('```json', "").replace("```", "")
        response = json.loads(response)
    except Exception as e:
        print(format_exc())
        pass
            
    return response