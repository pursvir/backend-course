from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import ObjectNotFoundException
from src.models.rooms import RoomsORM
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import RoomsDataMapper, RoomsWithRelsDataMapper
from src.repos.utils import room_ids_for_booking
from src.schemas.rooms import RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomsDataMapper

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)  # type: ignore
            .options(selectinload(self.model.facilities))  # type: ignore
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        row = result.scalars().one_or_none()
        if not row:
            return None
        return RoomsWithRelsDataMapper.map_to_domain_entity(row)

    async def get_one_with_rels(self, **filter_by):
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)  # type: ignore
        )
        result = await self.session.execute(query)
        try:
            row = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return RoomsWithRelsDataMapper.map_to_domain_entity(row)

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        room_ids = room_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))  # type: ignore
            .filter(RoomsORM.id.in_(room_ids))
        )
        result = await self.session.execute(query)
        return [
            RoomsWithRelsDataMapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]
