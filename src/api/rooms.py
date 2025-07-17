from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.exceptions import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.schemas.rooms import RoomAdd, RoomPatch, RoomPatchRequest, RoomRequestAdd
from src.services.rooms import RoomsService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Номера отеля", description="Получить все номера отеля")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(examples=["2024-05-01"]),
    date_to: date = Query(examples=["2024-05-10"]),
):
    return await RoomsService(db).get_rooms_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Номер отеля",
    description="Получить номер отеля",
)
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await RoomsService(db).get_room(room_id, hotel_id)
    except ObjectNotFoundException:
        # а отеля тоже...
        raise RoomNotFoundHTTPException


@router.post(
    "/{hotel_id}/rooms",
    summary="Новый номер",
    description="Добавить новый номер в отель",
)
async def add_room(db: DBDep, hotel_id: int, room_data: RoomRequestAdd = Body()):
    try:
        new_room_data = await RoomsService(db).add_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": new_room_data}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Изменить номер",
    description="Полная смена информации о номере",
)
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomRequestAdd):
    try:
        await RoomsService(db).edit_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частично изменить номер",
    description="Частичная смена информации о номере",
)
async def partially_edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    try:
        await RoomsService(db).edit_room_partially(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удалить номер",
    description="Удаление информации о номере",
)
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomsService(db).delete_room(room_id, hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}
