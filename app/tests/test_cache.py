import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.cache import CacheService
from app.models import Post
from app.schemas.schemas import PostCreate
from app.services import get_post_service, update_post_service, delete_post_service


@pytest.mark.asyncio
async def test_get_post_service_db_then_cache(
    cache: CacheService, async_db: AsyncSession
):
    post = Post(
        id=11,
        title="Test post",
        content="Test text",
        created_at=datetime.now(),
    )
    async_db.add(post)
    await async_db.commit()

    # первый вызов — поста нет в Redis, достаём из БД
    post_from_db = await get_post_service(11, cache, async_db)
    assert post_from_db is not None
    assert post_from_db.id == 11
    assert post_from_db.title == "Test post"

    # проверяем, что пост сохранился в Redis
    cached = await cache.get_post(11)
    assert cached is not None
    assert cached["title"] == "Test post"

    # второй вызов — пост достаётся уже из кеша
    post_from_cache = await get_post_service(11, cache, async_db)
    assert post_from_cache is not None
    assert post_from_cache.title == "Test post"


@pytest.mark.asyncio
async def test_cache_invalidation_on_update(
    cache: CacheService,
    async_db: AsyncSession,
):
    post = Post(
        id=22,
        title="Old title",
        content="Old content",
        created_at=datetime.now(),
    )
    async_db.add(post)
    await async_db.commit()

    # кладём в кеш
    await get_post_service(22, cache, async_db)
    cached_before = await cache.get_post(22)
    assert cached_before is not None

    # обновляем
    data = PostCreate(title="New title", content="New content")
    await update_post_service(22, data, cache, async_db)

    # кеш должен быть инвалидирован
    cached_after = await cache.get_post(22)
    assert cached_after is None

    # проверяем, что данные обновились
    updated = await get_post_service(22, cache, async_db)
    assert updated.title == "New title"


@pytest.mark.asyncio
async def test_cache_invalidation_on_delete(
    cache: CacheService, async_db: AsyncSession
):
    post = Post(
        id=33,
        title="Test title",
        content="Test content",
        created_at=datetime.now(),
    )
    async_db.add(post)
    await async_db.commit()

    # кладём в кеш
    await get_post_service(33, cache, async_db)
    cached_before = await cache.get_post(33)
    assert cached_before is not None

    # удаляем
    await delete_post_service(33, cache, async_db)

    # кеш должен быть удалён
    cached_after = await cache.get_post(33)
    assert cached_after is None
