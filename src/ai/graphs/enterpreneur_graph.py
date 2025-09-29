import asyncio
from typing import Annotated

from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph

from ai.tools.common import thinking_tool
from services.langgraph.db import Saver
from services.openai_agent import openai_llm_chat


class State(TypedDict):
    messages: Annotated[list, add_messages]
    

    
async def entrepreneur_chat_node(state: State):
    messages = await openai_llm_chat.ainvoke(state['messages'])
    return {"messages": messages}


async def entrepreneur_graph_builder() -> CompiledStateGraph:
    graph = StateGraph(State)
    graph.add_node("entrepreneur_chat_node", entrepreneur_chat_node)
    
    graph.add_edge(START, "entrepreneur_chat_node")
    graph.add_edge("entrepreneur_chat_node", END)
    
    return graph.compile(checkpointer=Saver.saver)

