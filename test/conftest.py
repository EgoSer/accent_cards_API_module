import os
from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def coalesce(value, default):
    return value if value else default


DATABASE_URL = coalesce(os.getenv("POSTGRES_URL"), "")

if DATABASE_URL == "":
    raise ValueError("Database URL is not provided!")

test_engine = create_async_engine(DATABASE_URL)
test_async_session_maker = async_sessionmaker(bind=test_engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session")
async def ensure_migrations():
    """Checks whether alembic migrations were made in test environment"""
    async with test_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    yield


@pytest_asyncio.fixture(scope="function", loop_scope="function")
async def db_session() -> AsyncGenerator[AsyncSession]:
    async with test_async_session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="class", loop_scope="class")
async def db_class_session() -> AsyncGenerator[AsyncSession]:
    async with test_async_session_maker() as session:
        yield session
        await session.rollback()
