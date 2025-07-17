from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    # first_name: Mapped[str] = mapped_column(String(32))
    # last_name: Mapped[str] = mapped_column(String(32))
    password_hash: Mapped[str] = mapped_column(String(128))
