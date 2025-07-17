from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService


class FacilitiesService(BaseService):
    async def get_all_facilities(self):
        facilities = await self.db.facilities.get_filtered()
        return facilities

    async def add_facility(self, facility_data: FacilityAdd):
        new_facility_data = await self.db.facilities.add(facility_data)
        await self.db.commit()
        return new_facility_data
