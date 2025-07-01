from datetime import date
from sqlalchemy import select

from src.repos.base import BaseRepository
from src.models.bookings import BookingsORM
from src.repos.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest

class BookingsRepository(BaseRepository):
    model = BookingsORM # type: ignore
    mapper = BookingDataMapper # type: ignore

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsORM)
            .filter(BookingsORM.date_from == date.today())
        )
        res = await self.session.execute()
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]
