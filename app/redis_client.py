from redis import asyncio as aioredis
from app.config import settings


# Initialize the Redis client
redis_client: aioredis.Redis = aioredis.from_url(
    settings.redis_url,
    decode_responses=True,  # Automatically decode responses to strings
)


def get_redis_client() -> aioredis.Redis:
    return redis_client
