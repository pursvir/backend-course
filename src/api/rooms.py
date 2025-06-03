from typing import List
from fastapi import APIRouter

from src.db import async_session_maker
from src.repos.rooms import RoomsRepository
from src.schemas.rooms import RoomRequestAdd, RoomAdd, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms", summary="Номера отеля", description="Получить все номера отеля")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)

@router.get("/{hotel_id}/rooms/{room_id}", summary="Номер отеля", description="Получить номер отеля")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)

@router.post("/{hotel_id}/rooms", summary="Новый номер", description="Добавить новый номер в отель")
async def add_room(hotel_id: int, room_data: RoomRequestAdd):
    new_room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(new_room_data)
        await session.commit()
    return {"status": "OK", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить номер", description="Полная смена информации о номере")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomRequestAdd):
    room_data_ = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data_, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично изменить номер", description="Частичная смена информации о номере")
async def partially_edit_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    room_data_ = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data_, partially_updated=True)
        await session.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер", description="Удаление информации о номере")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}
