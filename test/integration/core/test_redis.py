import pytest


@pytest.mark.asyncio
async def test_redis_write(redis_session):
    assert await redis_session.set("Test:key", "Test value")


@pytest.mark.asyncio
async def test_redis_decode(redis_session):
    value = await redis_session.get("Test:key")
    assert isinstance(value, str)


@pytest.mark.asyncio
async def test_redis_read(redis_session):
    value = await redis_session.get("Test:key")
    assert value == "Test value"
