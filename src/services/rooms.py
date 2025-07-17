from datetime import date
from re import L

from src.exceptions import (
    HotelNotFoundException,
    ObjectNotFoundException,
    RoomNotFoundException,
    check_date_to_after_date_from,
)
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import Room, RoomAdd, RoomPatch, RoomPatchRequest, RoomRequestAdd
from src.services.base import BaseService
from src.services.utils import get_hotel_with_check, get_room_with_check


class RoomsService(BaseService):
    async def get_rooms_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )

    async def get_room(self, room_id: int, hotel_id: int):
        return await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)

    async def add_room(self, hotel_id: int, room_data: RoomRequestAdd):
        await get_hotel_with_check(self.db, hotel_id)
        room_data_ = RoomAdd(
            hotel_id=hotel_id,
            **room_data.model_dump(exclude={"facilities_ids"}, exclude_none=True),
        )
        room: Room = await self.db.rooms.add(room_data_)  # pyright: ignore[reportAssignmentType]
        room_facilities_data = [
            RoomFacilityAdd(
                room_id=room.id,
                facility_id=facility_id,
            )
            for facility_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(room_facilities_data)
        await self.db.commit()

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomRequestAdd):
        room_data_ = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await get_hotel_with_check(self.db, hotel_id)
        await get_room_with_check(self.db, room_id)
        await self.db.rooms.edit(room_data_, id=room_id, hotel_id=hotel_id)
        await self.db.rooms_facilities.change_room_facilities(room_id, room_data.facilities_ids)
        await self.db.commit()

    async def edit_room_partially(self, hotel_id, room_id, room_data: RoomPatchRequest):
        room_data_ = RoomPatch(
            hotel_id=hotel_id,
            **room_data.model_dump(
                exclude_unset=True, exclude={"facilities_ids"}, exclude_none=True
            ),
        )
        await get_hotel_with_check(self.db, hotel_id)
        await get_room_with_check(self.db, room_id)
        await self.db.rooms.edit(room_data_, id=room_id, partially_updated=True)
        if room_data_.facilities_ids:
            await self.db.rooms_facilities.change_room_facilities(room_id, room_data.facilities_ids)
        await self.db.commit()

    async def delete_room(self, room_id: int, hotel_id: int):
        await get_hotel_with_check(self.db, hotel_id)
        await get_room_with_check(self.db, room_id)
        await self.db.rooms.delete(id=room_id)
        await self.db.commit()
