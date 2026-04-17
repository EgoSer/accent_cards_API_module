import uuid

from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(SA_UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4)

    @declared_attr.directive
    def __tablename__(self):
        return self.__name__.lower() + "s"


class Card(Base):
    pass
