import asyncio
import json
import logging
import redis

from channels.generic.websocket import AsyncWebsocketConsumer

from ai.publisher import log_route_event


logger = logging.getLogger("ai")


async def log_demo_msg():
    while True:
        await log_route_event("e40c62c3-0486-4a05-9b49-45876263166d", 'ideation_agent', "Testing")
        await asyncio.sleep(2)


class RouteTrackerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        await self.accept()

        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(f"route_updates:{self.session_id}")
        
        self.listen_task = asyncio.create_task(self.listen_to_redis())
        self.log_demo_msg = asyncio.create_task(log_demo_msg())


    async def listen_to_redis(self):
        """Continuously read messages from Redis and forward to client."""
        
        def blocking_listen(pubsub):
            for message in pubsub.listen():
                logger.info("Pubsub listing demo websocket message...")    
                if message['type'] == 'message':
                    yield message
        
        loop = asyncio.get_running_loop()
        while True:
            message = await asyncio.to_thread(lambda: next(blocking_listen(self.pubsub)))
            logger.info("Fetching demo websocket message...")
            data = json.loads(message['data'])
            await self.send_json(data=data)


    async def send_json(self, data) -> str:
        return await self.send(json.dumps(data))    


    async def disconnect(self, close_code):
        self.pubsub.close()
        self.redis.close()
        if hasattr(self, "listen_talk"):
            self.listen_task.cancel()
        if hasattr(self, "log_demo_msg"):
            self.log_demo_msg.cancel()