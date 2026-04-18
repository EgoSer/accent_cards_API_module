import os
from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


def coalesce(value, default):
    return value if value else default


class PGSettings(BaseSettings):
    USER: str | None
    PASSWORD: int | None
    HOST: str | None
    PORT: int | None
    DATABASE_NAME: str | None

    model_config = SettingsConfigDict()

    @cached_property
    def database_url(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE_NAME}"


pg_settings = PGSettings(
    USER=coalesce(os.getenv("POSTGRES_USER"), ""),
    PASSWORD=int(coalesce(os.getenv("POSTGRES_PASSWORD"), "")),
    HOST=coalesce(os.getenv("POSTGRES_HOST"), ""),
    PORT=int(coalesce(os.getenv("POSTGRES_PORT"), "")),
    DATABASE_NAME=coalesce(os.getenv("POSTGRES_DB"), ""),
)
