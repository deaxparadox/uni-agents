import json
import logging
from typing import (
    Any,
    Optional
)
import urllib

import aiohttp
from django.conf import settings
from langchain_core.tools import tool


logger = logging.getLogger("ai")


@tool
async def get_bubble_entreprenurs():
    """
    This function fetch the list of entreprenur from "The entrepreneur lab" site.
    """
    URL = f"{settings.BUBBLE_BASE_URL}/entrepreneur"
    HEADERS = {
        "Authorization": f"Bearer {settings.BUBBLE_API_KEY}",
        "Content-Type": "application/json",
    }
    logger.info("Making entrepreneur data request to entrepreneur lab...")
    
    data = None
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, headers=HEADERS) as response:
            logger.info(f"Entrepreneur response status code: {response.status}")
            data = await response.json()
            # logger.debug(f"Response data: {data}")
            
    return data


@tool
async def get_bubble_freelancers(email: Optional[str] = None) -> Any:
    """
    This function fetch the list of freelancer from "The entrepreneur lab" site.
    
    You can use filter also, if required:
    email: use this filter to search freelancer by email
    
    Args:
        email: Email of freelancer to search
    """
    logger.info(f"Freelancer email: {email}")
    
    
    URL = f"{settings.BUBBLE_BASE_URL}/freelancer"
    HEADERS = {
        "Authorization": f"Bearer {settings.BUBBLE_API_KEY}",
        "Content-Type": "application/json",
    }
    logger.info("Making entrepreneur data request to entrepreneur lab...")
    
    if email:
        constraints = [
            {
                "key": "email",
                "constraint_type": "equals",
                "value": email
            }
        ]
        constraints_param = urllib.parse.quote(json.dumps(constraints))
        URL = f"{URL}?constraints={constraints_param}"
    
    
    
    data = None
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, headers=HEADERS) as response:
            logger.info(f"Freelancer response status code: {response.status}")
            data = await response.json()
            logger.debug(f"Response data: {data}")
            
    return data