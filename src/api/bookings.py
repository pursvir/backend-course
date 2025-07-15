from fastapi import APIRouter
from starlette.exceptions import HTTPException

from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.rooms import Room
from src.schemas.hotels import Hotel
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
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)  # pyright: ignore[reportAssignmentType]
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    hotel: Hotel | None = await db.hotels.get_one(id=room.hotel_id)  # pyright: ignore[reportAssignmentType, reportOptionalMemberAccess]
    price: int = room.price  # pyright: ignore[reportOptionalMemberAccess]
    booking_data_add = BookingAdd(user_id=user_id, price=price, **booking_data.model_dump())
    try:
        new_booking_data = await db.bookings.add_booking(
            booking_data_add,
            hotel_id=hotel.id,  # pyright: ignore[reportOptionalMemberAccess]
        )
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    finally:
        await db.commit()
    return {"status": "OK", "data": new_booking_data}
