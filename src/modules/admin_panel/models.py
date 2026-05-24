from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.sql.database import Base


class Admin(Base):
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[bytes]
