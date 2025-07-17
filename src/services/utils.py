from src.exceptions import HotelNotFoundException, ObjectNotFoundException, RoomNotFoundException
from src.utils.db_manager import DBManager


async def get_hotel_with_check(db: DBManager, hotel_id: int):
    try:
        return await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundException


async def get_room_with_check(db: DBManager, room_id: int):
    try:
        return await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundException
