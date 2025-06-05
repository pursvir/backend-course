from typing import List
from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.rooms import (
    RoomRequestAdd, RoomAdd,
    RoomPatchRequest, RoomPatch
)

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms", summary="Номера отеля", description="Получить все номера отеля")
async def get_rooms(db: DBDep, hotel_id: int):
     return await db.rooms.get_filtered(hotel_id=hotel_id)

@router.get("/{hotel_id}/rooms/{room_id}", summary="Номер отеля", description="Получить номер отеля")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)

@router.post("/{hotel_id}/rooms", summary="Новый номер", description="Добавить новый номер в отель")
async def add_room(db: DBDep, hotel_id: int, room_data: RoomRequestAdd):
    new_room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(new_room_data)
    await db.commit()
    return {"status": "OK", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить номер", description="Полная смена информации о номере")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomRequestAdd):
    room_data_ = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(room_data_, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично изменить номер", description="Частичная смена информации о номере")
async def partially_edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    room_data_ = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(room_data_, partially_updated=True)
    await db.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер", description="Удаление информации о номере")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
