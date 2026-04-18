import os
from functools import cached_property

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


def coalesce(value, default):
    return value if value else default


class PGSettings(BaseSettings):
    USER: str | None
    PASSWORD: str | None
    HOST: str | None
    PORT_POOLER: int | None
    PORT_DATABASE: int | None
    DATABASE_NAME: str | None

    model_config = SettingsConfigDict()

    @cached_property
    def database_url(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT_DATABASE}/{self.DATABASE_NAME}"

    @cached_property
    def database_pooler_url(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT_POOLER}/{self.DATABASE_NAME}"


pg_settings = PGSettings(
    USER=coalesce(os.getenv("POSTGRES_USER"), ""),
    PASSWORD=coalesce(os.getenv("POSTGRES_PASSWORD"), ""),
    HOST=coalesce(os.getenv("POSTGRES_HOST"), ""),
    PORT_POOLER=int(coalesce(os.getenv("PGBOUNCER_PORT"), "")),
    PORT_DATABASE=int(coalesce(os.getenv("POSTGRES_PORT"), "")),
    DATABASE_NAME=coalesce(os.getenv("POSTGRES_DB"), ""),
)

logger.debug(f"Created settings object: {pg_settings}")
