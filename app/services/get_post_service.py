from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.cache import CacheService
from app.models import Post
from app.schemas.schemas import PostOut


async def get_post_service(
    post_id: int, cache: CacheService, db: AsyncSession
) -> PostOut:
    post_cached = await cache.get_post(post_id)
    if post_cached:
        return PostOut(**post_cached)

    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    post_db = result.scalar_one_or_none()
    if not post_db:
        raise HTTPException(status_code=404, detail="Post not found")

    value = {
        "id": post_db.id,
        "title": post_db.title,
        "content": post_db.content,
        "created_at": post_db.created_at.isoformat(),
    }

    await cache.set_post(post_id, value)
    return PostOut(**value)
