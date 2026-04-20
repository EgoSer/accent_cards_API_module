import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


def coalesce(value, default):
    return value if value else default


DATABASE_URL = coalesce(os.getenv("POSTGRES_URL"), "")

if DATABASE_URL == "":
    raise ValueError("Database URL is not provided!")


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def test_engine() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(DATABASE_URL)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def test_async_session_maker(test_engine: AsyncEngine):
    return async_sessionmaker(bind=test_engine, expire_on_commit=True)


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def ensure_migrations():
    """Checks whether alembic migrations were made in test environment"""
    async with test_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    yield


@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def db_session() -> AsyncGenerator[AsyncSession]:
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
