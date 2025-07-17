from fastapi import APIRouter
from kombu.abstract import Object
from starlette.exceptions import HTTPException

from src.api.dependencies import DBDep, UserIDDep
from src.exceptions import (
    AllRoomsAreBookedException,
    AllRoomsAreBookedHTTPException,
    ObjectNotFoundException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.services.bookings import BookingsService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingsService(db).get_all_bookings()


@router.get("/me")
async def get_bookings_me(db: DBDep, user_id: UserIDDep):
    return await BookingsService(db).get_filtered_bookings(user_id)


@router.post("")
async def add_booking(db: DBDep, user_id: UserIDDep, booking_data: BookingAddRequest):
    try:
        new_booking_data = await BookingsService(db).add_booking(user_id, booking_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomsAreBookedException as ex:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": new_booking_data}
