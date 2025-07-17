from sqlalchemy import func, select

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import HotelDataMapper
from src.repos.utils import room_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        location,
        title,
        limit,
        offset,
        date_from,
        date_to,
    ):
        room_ids = room_ids_for_booking(date_from=date_from, date_to=date_to)
        hotel_ids = (
            select(RoomsORM.hotel_id).select_from(RoomsORM).filter(RoomsORM.id.in_(room_ids))
        )

        query = select(HotelsORM).select_from(HotelsORM).filter(HotelsORM.id.in_(hotel_ids))
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(row) for row in result.scalars().all()]
