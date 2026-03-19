from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.cache import CacheService
from app.models import Post


async def delete_post_service(post_id: int, cache: CacheService, db: AsyncSession):
    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    post_db = result.scalar_one_or_none()
    if not post_db:
        raise HTTPException(status_code=404, detail="Post not found")
    await db.delete(post_db)
    await db.commit()
    await cache.invalidate_post(post_id)
