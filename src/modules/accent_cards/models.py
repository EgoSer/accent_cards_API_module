from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.sql.database import Base


class Card(Base):
    word: Mapped[str] = mapped_column(String, unique=True)
    accent: Mapped[int] = mapped_column(SmallInteger)
