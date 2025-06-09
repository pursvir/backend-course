from sqlalchemy import delete

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repos.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility

    async def delete_bulk_ids(self, ids: list[int]) -> None:
        if ids is None:
            return
        delete_stmt = (
            delete(self.model)
            .filter(self.model.facility_id.in_(ids))
        )
        await self._session.execute(delete_stmt)
