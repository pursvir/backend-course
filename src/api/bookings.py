from fastapi import APIRouter

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIDDep

router = APIRouter(prefix="/bookings", tags=["Бронирование"])

@router.post("")
async def add_booking(db: DBDep, user_id: UserIDDep, booking_data: BookingAddRequest):
    price = (
        await db.rooms.get_one(id=booking_data.room_id)
    ).model_dump()["price"]
    print(booking_data.model_dump())
    booking_data_ = BookingAdd(user_id=user_id, price=price, **booking_data.model_dump())
    new_booking_data = await db.bookings.add(booking_data_)
    return {"status": "OK", "data": new_booking_data}
