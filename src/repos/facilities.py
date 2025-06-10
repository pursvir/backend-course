from sqlalchemy import select, insert, delete

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repos.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility

    async def change_room_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
        current_room_facility_ids_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        result = await self._session.execute(current_room_facility_ids_query)
        current_facilities_ids: list[int] = result.scalars().all()

        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_add: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete)
                )
            )
            await self._session.execute(delete_m2m_facilities_stmt)
        if ids_to_add:
            add_m2m_facilities_stmt = (
                insert(self.model)
                .values([
                    {"room_id": room_id, "facility_id": facility_id} \
                    for facility_id in facilities_ids
                ])
            )
            await self._session.execute(add_m2m_facilities_stmt)
