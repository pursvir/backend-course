from datetime import date
from fastapi import APIRouter, Query, Body
from fastapi.exceptions import HTTPException

from src.api.dependencies import DBDep
from src.exceptions import ObjectNotFoundException, ObjectAddConflictException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import Room, RoomRequestAdd, RoomAdd, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Номера отеля", description="Получить все номера отеля")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(examples=["2024-05-01"]),
    date_to: date = Query(examples=["2024-05-10"]),
):
    if date_from > date_to:
        raise HTTPException(status_code=400, detail="Дата заезда не может быть позже даты выезда")
    return await db.rooms.get_filtered_by_time(
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
        return await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Данного отеля не существует")


@router.post(
    "/{hotel_id}/rooms",
    summary="Новый номер",
    description="Добавить новый номер в отель",
)
async def add_room(db: DBDep, hotel_id: int, room_data: RoomRequestAdd = Body()):
    room_data_ = RoomAdd(
        hotel_id=hotel_id,
        **room_data.model_dump(exclude={"facilities_ids"}, exclude_none=True),
    )
    try:
        room: Room = await db.rooms.add(room_data_)  # pyright: ignore[reportAssignmentType]
    except ObjectAddConflictException:
        raise HTTPException(status_code=409, detail="Данного отеля не существует")

    # Тут по-хорошему ещё обрабатывать несуществующие facilities, но раз в задании этого нет, то нет :)
    room_facilities_data = [
        RoomFacilityAdd(
            room_id=room.id,
            facility_id=facility_id,
        )
        for facility_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(room_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Изменить номер",
    description="Полная смена информации о номере",
)
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomRequestAdd):
    room_data_ = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        await db.rooms.edit(room_data_, id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Данного номера не существует")
    await db.rooms_facilities.change_room_facilities(room_id, room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частично изменить номер",
    description="Частичная смена информации о номере",
)
async def partially_edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    room_data_ = RoomPatch(
        hotel_id=hotel_id,
        **room_data.model_dump(exclude_unset=True, exclude={"facilities_ids"}, exclude_none=True),
    )
    try:
        await db.rooms.edit(room_data_, id=room_id, partially_updated=True)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Данного номера не существует")
    if room_data_.facilities_ids:
        await db.rooms_facilities.change_room_facilities(room_id, room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удалить номер",
    description="Удаление информации о номере",
)
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Данного номера не существует")
    await db.commit()
    return {"status": "OK"}
