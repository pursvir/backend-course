from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from sqlalchemy.util.langhelpers import hybridproperty

from src.db import Base

class BookingsORM(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]

    @hybridproperty
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days
