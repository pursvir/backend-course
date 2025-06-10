from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.db import engine
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
from src.repos.base import BaseRepository
from src.repos.utils import room_ids_for_booking
from src.schemas.rooms import Room, RoomsWithRels


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self._session.execute(query)
        row = result.scalars().one_or_none()
        if not row:
            return None
        return RoomsWithRels.model_validate(row)

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date
    ):
        room_ids = room_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(room_ids))
        )
        result = await self._session.execute(query)
        return [RoomsWithRels.model_validate(model) for model in result.scalars().all()]
