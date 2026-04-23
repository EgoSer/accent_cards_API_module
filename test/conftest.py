from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
import redis.asyncio as redis
from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.core.redis.config import redis_settings
from src.core.sql.config import pg_settings

DATABASE_URL = pg_settings.database_url

if DATABASE_URL == "":
    raise ValueError("Database URL is not provided!")


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def test_engine() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(DATABASE_URL)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
def test_async_session_maker(test_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=test_engine, expire_on_commit=True, class_=AsyncSession)


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def ensure_migrations(test_engine: AsyncEngine) -> AsyncGenerator[None]:
    """Checks whether alembic migrations were made in test environment"""
    async with test_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    yield


@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def db_session(
    test_engine: AsyncEngine, test_async_session_maker: async_sessionmaker[AsyncSession]
) -> AsyncGenerator[AsyncSession]:
    connection = await test_engine.connect()
    transaction = await connection.begin()
    session = test_async_session_maker(bind=connection)

    logger.info("[Setup] New session and transaction created")

    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()
        logger.info("[Teardown] All changes reverted")


@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def get_db_session_generator():
    yield db_session


@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def redis_session() -> AsyncGenerator[redis.Redis]:
    redis_client = redis.Redis(
        host=redis_settings.REDIS_HOST,
        port=redis_settings.REDIS_PORT,
        username=redis_settings.REDIS_USER,
        password=redis_settings.REDIS_PASSWORD,
        db=redis_settings.REDIS_DB,
        encoding="utf-8",
        decode_responses=True,
    )

    try:
        await redis_client.ping()  # type: ignore
    except redis.ConnectionError as e:
        logger.error(f"Couldn't connect to redis. URL: {redis_settings.get_url}")
        raise e

    logger.info("New redis session created")

    try:
        yield redis_client
    except Exception as e:
        logger.error(f"An unexpected exception occured during redis session: {e}")
        raise e
    finally:
        await redis_client.aclose()
        logger.info("Redis session closed")
