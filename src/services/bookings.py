from src.exceptions import HotelNotFoundException, ObjectNotFoundException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.services.base import BaseService
from src.services.utils import get_room_with_check


class BookingsService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_filtered_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(self, user_id: int, booking_data: BookingAddRequest):
        room: Room = await get_room_with_check(self.db, booking_data.room_id)  # type: ignore
        try:
            hotel: Hotel | None = await self.db.hotels.get_one(id=room.hotel_id)  # pyright: ignore[reportAssignmentType, reportOptionalMemberAccess]
        except ObjectNotFoundException:
            raise HotelNotFoundException
        price: int = room.price  # pyright: ignore[reportOptionalMemberAccess]
        booking_data_add = BookingAdd(user_id=user_id, price=price, **booking_data.model_dump())
        new_booking_data = await self.db.bookings.add_booking(
            booking_data_add,
            hotel_id=hotel.id,  # pyright: ignore[reportOptionalMemberAccess]
        )
        await self.db.commit()
        return new_booking_data
