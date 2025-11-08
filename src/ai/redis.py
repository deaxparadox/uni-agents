import os

from dotenv import load_dotenv
import redis
import redis.asyncio as aredis

load_dotenv()

redis_client = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=3)
aredis_client = aredis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=4)