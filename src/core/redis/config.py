import os
from functools import cached_property

from pydantic_settings import BaseSettings


def coalesce(value, default):
    return value if value else default


class RedisSettings(BaseSettings):
    REDIS_PASSWORD: str
    REDIS_USER: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    @cached_property
    def get_url(self):
        return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


redis_pass = coalesce(os.getenv("REDIS_PASSWORD"), "")
redis_host = coalesce(os.getenv("REDIS_HOST"), "")

redis_settings = RedisSettings(
    REDIS_PASSWORD=redis_pass, REDIS_HOST=redis_host, REDIS_USER="", REDIS_PORT=6379, REDIS_DB=0
)
