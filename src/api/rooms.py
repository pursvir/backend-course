from datetime import date
from fastapi import APIRouter, Query, Body

from src.api.dependencies import DBDep
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
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


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
    room: Room = await db.rooms.add(room_data_)  # pyright: ignore[reportAssignmentType]

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
    await db.rooms.edit(room_data_, id=room_id, hotel_id=hotel_id)
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
    await db.rooms.edit(room_data_, id=room_id, partially_updated=True)
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
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
