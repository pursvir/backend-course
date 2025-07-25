from typing import Sequence

from sqlalchemy import delete, insert, select

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import FacilitiesDataMapper, RoomsFacilityDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    mapper = RoomsFacilityDataMapper

    async def change_room_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
        current_room_facility_ids_query = select(self.model.facility_id).filter_by(  # type: ignore
            room_id=room_id
        )
        result = await self.session.execute(current_room_facility_ids_query)
        current_facilities_ids: Sequence[int] = result.scalars().all()

        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_add: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities_stmt = delete(self.model).filter(  # type: ignore
                self.model.room_id == room_id,  # type: ignore
                self.model.facility_id.in_(ids_to_delete),  # type: ignore
            )
            await self.session.execute(delete_m2m_facilities_stmt)
        if ids_to_add:
            add_m2m_facilities_stmt = insert(self.model).values(  # type: ignore
                [{"room_id": room_id, "facility_id": facility_id} for facility_id in facilities_ids]
            )
            await self.session.execute(add_m2m_facilities_stmt)
