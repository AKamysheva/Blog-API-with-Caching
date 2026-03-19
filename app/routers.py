from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import PostCreate, PostOut
from app.db.database import get_db
from app.models import Post
from app.cache import CacheService, get_cache_service
from app.services import get_post_service, update_post_service, delete_post_service


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[PostOut])
async def get_all_posts(db: AsyncSession = Depends(get_db)):
    stmt = select(Post)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{post_id}", response_model=PostOut)
async def get_post(
    post_id: int,
    cache: CacheService = Depends(get_cache_service),
    db: AsyncSession = Depends(get_db),
):
    return await get_post_service(post_id, cache, db)


@router.post("/create-post", response_model=PostOut)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    post = Post(title=post.title, content=post.content)
    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post


@router.put("/update-post/{post_id}", response_model=PostOut)
async def update_post(
    post_id: int,
    post: PostCreate,
    cache: CacheService = Depends(get_cache_service),
    db: AsyncSession = Depends(get_db),
):
    return await update_post_service(post_id, post, cache, db)


@router.delete("/delete-post/{post_id}")
async def delete_post(
    post_id: int,
    cache: CacheService = Depends(get_cache_service),
    db: AsyncSession = Depends(get_db),
):
    return await delete_post_service(post_id, cache, db)
