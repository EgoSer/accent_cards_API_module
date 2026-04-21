from collections.abc import AsyncGenerator

from loguru import logger

import redis.asyncio as redis

from .config import redis_settings


async def async_redis_session() -> AsyncGenerator[redis.Redis]:
    redis_client = redis.Redis(
        host=redis_settings.REDIS_HOST,
        port=redis_settings.REDIS_PORT,
        username=redis_settings.REDIS_USER,
        password=redis_settings.REDIS_PASSWORD,
        db=redis_settings.REDIS_DB,
        encoding="ascii",
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
