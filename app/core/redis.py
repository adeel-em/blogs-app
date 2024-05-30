import redis.asyncio as redis
import asyncio
from app.core.config import settings


class RedisClient:
    _instance = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = redis.from_url(settings.REDIS_URL, decode_responses=True)
        return cls._instance

    @classmethod
    async def close_instance(cls):
        if cls._instance:
            await cls._instance.close()
            cls._instance = None


# Make sure to close the Redis connection on shutdown
async def on_shutdown():
    await RedisClient.close_instance()
