from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph

from ai.prompts.enterpreneur_assistant import enterpreneur_agent_prompt
from services.openai_agent import openai_llm_chat

class State(TypedDict):
    messages = Annotated[list, add_messages]
    

async def enterpreneur_agent(state: State):
    return {"messages": openai_llm_chat.ainvoke(state['messages'])}


async def graph_builder() -> CompiledStateGraph:
    graph = StateGraph(State)
    graph.add_node("enterpreneur_agent", enterpreneur_agent)
    
    graph.add_edge(START, "enterpreneur_agent")
    graph.add_edge("enterpreneur_agent", END)

    return graph.compile()


async def stream_graph_updates(user_input: str, system_prompt: str = enterpreneur_agent_prompt):
    graph: CompiledStateGraph = graph_builder()
    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": user_input}
    ]
    for event in graph.stream({"messages": messages}):
        for value in event.values:
            print("Assistant:", value['messages'][-1].content)