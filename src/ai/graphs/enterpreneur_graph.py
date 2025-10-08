import asyncio
from typing import Annotated

from langgraph.graph import END, StateGraph, START
from langgraph.graph.state import CompiledStateGraph

from ai.state import State
from ai.prompts.entrepreneur_router_prompt import entrepreneur_router_prompt
from services.langgraph.db import Saver
from services.openai_agent import openai_llm_chat





async def entrepreneur_router_agent(state: State):
    user_query = state['user_query']
    messages = [
        {"role": "system", "content": entrepreneur_router_prompt},
        {"role": "user", "content": entrepreneur_router_prompt}
    ]
    await openai_llm_chat.llm.ainvoke(messages = messages)
    
    

    
async def entrepreneur_chat_node(state: State):
    messages = await openai_llm_chat.ainvoke(state['messages'])
    return {"messages": messages}


async def entrepreneur_graph_builder() -> CompiledStateGraph:
    graph = StateGraph(State)
    graph.add_node("entrepreneur_chat_node", entrepreneur_chat_node)
    graph.add_node("entrepreneur_router_agent", entrepreneur_router_agent)
    
    graph.add_edge(START, "entrepreneur_chat_node")
    graph.add_edge("entrepreneur_chat_node", END)
    
    return graph.compile(checkpointer=Saver.saver)

