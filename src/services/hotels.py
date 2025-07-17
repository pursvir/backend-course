from datetime import date

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import check_date_to_after_date_from
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.base import BaseService


class HotelsService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination: PaginationDep,
        location: str | None,
        title: str | None,
        date_from: date,
        date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        hotels = await self.db.hotels.get_filtered_by_time(
            location,
            title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            date_from=date_from,
            date_to=date_to,
        )
        return hotels

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, hotel_data: HotelAdd):
        await self.db.hotels.add(hotel_data)
        await self.db.commit()

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

    async def edit_hotel_partially(self, hotel_id: int, hotel_data: HotelPatch):
        await self.db.hotels.edit(hotel_data, id=hotel_id, partially_updated=True)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
