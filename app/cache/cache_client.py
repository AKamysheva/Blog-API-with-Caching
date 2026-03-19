from app.redis_client import redis_client
from app.cache import CacheService


cache_service = CacheService(redis_client)


def get_cache_service():
    return cache_service
