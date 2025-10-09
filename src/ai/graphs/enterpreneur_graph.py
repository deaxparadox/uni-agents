import asyncio
import json
import logging
from typing import Annotated

from langgraph.graph import END, StateGraph, START
from langgraph.graph.state import CompiledStateGraph

from ai.state import State
from ai.prompts.entrepreneur_router_prompt import entrepreneur_router_prompt
from ai.prompts.entrepreneur_roadmap_prompt import cofounder_agent_prompt
from ai.prompts.entrepreneur_ideation_prompt import cofounder_ideation_agent_prompt
from services.langgraph.db import Saver
from services.openai_agent import openai_llm_chat


logger = logging.getLogger("ai")


async def user_query_node(state: State):
    return {"messages": [{"role": "user", "content": state['user_query']}]}
    


async def entrepreneur_router_agent(state: State):
    logger.debug("1111111111111111111111111111111")
    user_query = state['user_query']
    chat_id = state['chat_id']
    logger.info(f"User query: {user_query}")
    
    messages = [
        {"role": "system", "content": entrepreneur_router_prompt},
        {"role": "user", "content": user_query}
    ]
    
    response = await openai_llm_chat.ainvoke(messages, config={'configurable': {"thread_id": chat_id}}, stream=False)
    response_content = response.content
    response_content_string = response_content.replace("```json", "").replace("```", "")
    response = json.loads(response_content_string)
    logger.info(f"Router agent response: {response}")
    state["router_response"] = response
    return state

async def entrepneur_conditional_node(state: State):
    logger.debug("2222222222222222222222222222222222")
    router_response = state['router_response']
    next_node = router_response['recommended_node']
    logger.info(f"Conditional agent response:, {next_node}")
    return next_node
    
    
async def entrepreneur_chat_node(state: State):
    messages = await openai_llm_chat.ainvoke(state['messages'])
    return {"messages": messages}


async def entrepreneur_roadmap_agent(state: State):
    logger.debug("333333333333333333333333333333333333333")
    user_query = state['user_query']
    chat_id = state["chat_id"]
    
    messages = [
        {"role": "system", "content": cofounder_agent_prompt},
        {"role": "user", "content": user_query}
    ]
    
    response = await openai_llm_chat.ainvoke(messages, config={'configurable': {"thread_id": chat_id}})
    response_content = response.content
    response_content_string = response_content.replace("```json", "").replace("```", "")
    response = json.loads(response_content_string)
    logger.info(f"Roadmap agent response: {response}")
    state["final_response"] = response
    return {
        "messages": [
            {"role": "assistant", "content": response_content_string}
        ]
    }
    
async def entrepreneur_ideation_agent(state: State):
    logger.debug("44444444444444444444444444444444444444444")
    user_query = state['user_query']
    chat_id = state["chat_id"]
    
    messages = [
        {"role": "system", "content": cofounder_ideation_agent_prompt},
        {"role": "user", "content": user_query}
    ]
    
    response = await openai_llm_chat.ainvoke(messages, config={'configurable': {"thread_id": chat_id}})
    response_content = response.content
    logger.info(f"Ideation agent content:, {response_content}, {type(response_content)}")
    response_content_string = response_content.replace("```json", "").replace("```", "")
    response = json.loads(response_content_string)
    logger.info(f"Ideation agent response: {response}")
    state["final_response"] = response
    return {
        "messages": [
            {"role": "assistant", "content": response_content_string}
        ]
    }
    


async def entrepreneur_graph_builder() -> CompiledStateGraph:
    graph = StateGraph(State)
    graph.add_node("user_query_node", user_query_node)
    graph.add_node("entrepreneur_chat_node", entrepreneur_chat_node)
    graph.add_node("entrepreneur_router_agent", entrepreneur_router_agent)
    graph.add_node("entrepreneur_roadmap_agent", entrepreneur_roadmap_agent)
    graph.add_node("entrepreneur_ideation_agent", entrepreneur_ideation_agent)
    
    graph.add_edge(START, "user_query_node")
    graph.add_edge("user_query_node", "entrepreneur_router_agent")
    # graph.add_edge("entrepreneur_router_agent", END)
    graph.add_conditional_edges("entrepreneur_router_agent", entrepneur_conditional_node)
    
    # graph.add_edge("entrepreneur_router_agent", "entrepreneur_chat_node")
    # graph.add_edge("entrepreneur_chat_node", END)
    
    return graph.compile(checkpointer=Saver.saver)

