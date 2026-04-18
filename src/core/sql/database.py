import uuid

from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from core.sql.config import pg_settings

engine = create_async_engine(pg_settings.database_url)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4)

    @declared_attr.directive
    def __tablename__(self):
        return self.__name__.lower() + "s"
