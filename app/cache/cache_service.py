import json
from app.config import settings


class CacheService:
    def __init__(self, redis):
        self.redis = redis

    @staticmethod
    def create_key(post_id: int) -> str:
        return f"post:{str(post_id)}"

    async def get_post(self, post_id: int):
        data = await self.redis.get(self.create_key(post_id))
        if data:
            return json.loads(data)
        return None

    async def set_post(self, post_id: int, value: dict, ttl: int = settings.CACHE_TTL):
        await self.redis.set(
            self.create_key(post_id),
            json.dumps(value),
            ex=ttl,
        )

    async def invalidate_post(self, post_id: int):
        await self.redis.delete(self.create_key(post_id))
