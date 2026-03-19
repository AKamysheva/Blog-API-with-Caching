from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.cache import CacheService
from app.models import Post
from app.schemas.schemas import PostOut


async def update_post_service(
    post_id: int, data, cache: CacheService, db: AsyncSession
):
    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    post_db = result.scalar_one_or_none()
    if not post_db:
        raise HTTPException(status_code=404, detail="Post not found")
    post_db.title = data.title
    post_db.content = data.content

    await db.commit()
    await cache.invalidate_post(post_id)
    return PostOut.model_validate(post_db)
