# JWT tokens validation
import hashlib
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt
from loguru import logger

from src.core.redis.dependencies import async_redis_session

from .env import JWT_algorithm, JWT_secret


async def is_blacklisted(value) -> bool:
    try:
        async with async_redis_session() as redis_session:
            value = value.strip()
            value_hash = hashlib.sha256(value.encode()).hexdigest()[:16]
            value_status = await redis_session.get(f"blacklisted:{value_hash}")
            if value_status is None:
                return False
            return True
    except Exception as e:
        logger.error(f"Trying to validate if value {value} blacklisted: {e}")
        raise e


async def blacklist(value, expire_in):
    try:
        async with async_redis_session() as redis_session:
            value = value.strip()
            value_hash = hashlib.sha256(value.encode()).hexdigest()[:16]
            await redis_session.setex(f"blacklisted:{value_hash}", expire_in * 60, True)
            logger.info(f"Blacklisted value with hash {value_hash}")
    except Exception as e:
        logger.error(f"Trying to blacklist value {value}: {e}")
        return False
    return True


async def check_token(token: str) -> Any | None:
    try:
        if await is_blacklisted(token):
            return None
    except Exception as e:
        return None
    try:
        payload = jwt.decode(token, JWT_secret, algorithms=[JWT_algorithm], options={"verify_sub": False})
    except Exception as e:
        logger.error(f"Trying to validate JWT token: {e}")
        return None
    return payload


async def create_token(data: dict, expire_in: int):
    payload = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=expire_in)
    payload.update({"exp": expire})
    return jwt.encode(payload, JWT_secret, algorithm=JWT_algorithm)
