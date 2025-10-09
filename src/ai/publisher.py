
import json
import redis
import logging
from datetime import datetime, timezone
from typing import Literal


logger = logging.getLogger("ai")

r = redis.Redis(host='localhost', port=6379, db=0)

async def log_route_event(session_id, agent: Literal['router_agent', "roadmap_agent", "ideation_agent"], action: str, details: str | None = None):
    """Publish a new event to Redis"""
    message = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "action": action,
        "details": details,
    }
    logger.info("Publish... demo msg")
    r.publish(f"route_updates:{session_id}", json.dumps(message))
