from datetime import date

from sqlalchemy import select

from src.exceptions import AllRoomsAreBookedException
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import BookingDataMapper, RoomsDataMapper
from src.repos.utils import room_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsORM).filter(BookingsORM.date_from == date.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        room_ids = room_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )
        rooms_availabe_query = (
            select(RoomsORM)
            .select_from(RoomsORM)
            .filter(RoomsORM.id == data.room_id)
            .filter(RoomsORM.id.in_(room_ids))
        )
        result = await self.session.execute(rooms_availabe_query)
        res = [RoomsDataMapper.map_to_domain_entity(row) for row in result.scalars().all()]
        if res == []:
            raise AllRoomsAreBookedException
        await super().add(data)
