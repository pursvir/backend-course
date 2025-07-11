from fastapi import APIRouter

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIDDep

router = APIRouter(prefix="/bookings", tags=["Бронирование"])

@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()

@router.get("/me")
async def get_bookings_me(db: DBDep, user_id: UserIDDep):
    return await db.bookings.get_filtered(user_id=user_id)

@router.post("")
async def add_booking(db: DBDep, user_id: UserIDDep, booking_data: BookingAddRequest):
    room = await db.rooms.get_one(id=booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id) # type: ignore
    price: int = room.price # type: ignore
    booking_data_add = BookingAdd(
        user_id=user_id,
        price=price,
        **booking_data.model_dump()
    )
    new_booking_data = await db.bookings.add_booking(booking_data_add, hotel_id=hotel.id) # type: ignore
    await db.commit()
    return {"status": "OK", "data": new_booking_data}
