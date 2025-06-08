from datetime import date
from sqlalchemy import select, func

from src.db import engine
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
from src.repos.base import BaseRepository
from src.repos.utils import room_ids_for_booking
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date
    ):
        room_ids = room_ids_for_booking(date_from, date_to, hotel_id)
        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        return await self.get_filtered(RoomsORM.id.in_(room_ids))
