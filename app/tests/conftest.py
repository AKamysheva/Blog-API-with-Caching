import pytest_asyncio
import fakeredis.aioredis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.db.database import Base
from app.cache import CacheService


DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

testing_async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture
async def cache():
    redis = await fakeredis.aioredis.FakeRedis(decode_responses=True)
    service = CacheService(redis)
    yield service
    await redis.aclose()


@pytest_asyncio.fixture
async def async_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with testing_async_session() as session:
        yield session

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
