from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi.exceptions import HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import (
    HotelAlreadyExistsException,
    HotelAlreadyExistsHTTPException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
)
from src.schemas.fields import pos_int
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.hotels import HotelsService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение отелей",
    description="<h3>Тут мы можем запросить данные об отелях в базе. В query опционально можно указать ID, title, name.\
    Также поддерживается пагинация, где page - порядковый номер страницы, а per_page - сколько вы хотите получить отелей в ответе</h3>",
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Hotel name"),
    location: str | None = Query(None, description="Hotel location"),
    date_from: date = Query(examples=["2025-06-01"]),
    date_to: date = Query(examples=["2025-06-12"]),
):
    hotels = await HotelsService(db).get_filtered_by_time(
        pagination, location, title, date_from, date_to
    )
    return {"status": "OK", "data": hotels}


@router.get(
    "/{hotel_id}",
    summary="Получить отель",
    description="<h3>Тут мы можем получить отель по ID-шнику из базы.</h3>",
)
async def get_hotel(db: DBDep, hotel_id: pos_int):
    try:
        return await HotelsService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post(
    "",
    summary="Добавление отеля",
    description="<h3>Тут мы добавляем новый отель: нужно отправить name и title</h3>",
)
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звёзд у моря",
                    "location": "ул. Моря, 2",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай 5 звёзд у фонтана",
                    "location": "ул. Шейха, 3",
                },
            },
        }
    ),
):
    try:
        new_hotel = await HotelsService(db).add_hotel(hotel_data)
    except HotelAlreadyExistsException:
        raise HotelAlreadyExistsHTTPException
    return {"status": "OK", "data": new_hotel}


@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных об отеле по ID",
    description="<h3>Тут мы полностью перезаписываем данные об отеле с указанным ID: можно отправить name, а можно title, а можно вообще ничего</h3>",
)
async def put_hotel(
    db: DBDep,
    hotel_id: pos_int,
    hotel_data: HotelAdd,
):
    try:
        await HotelsService(db).edit_hotel(hotel_id, hotel_data)
        return {"status": "OK"}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.patch(
    "/hotels/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h3>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title, а можно вообще ничего</h3>",
)
async def patch_hotel(db: DBDep, hotel_id: pos_int, hotel_data: HotelPatch):
    try:
        await HotelsService(db).edit_hotel_partially(hotel_id, hotel_data)
        return {"status": "OK"}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля по ID",
    description="<h3>Отель, ID которого будет указан в path, будет удалён из базы</h3>",
)
async def delete_hotel(db: DBDep, hotel_id: pos_int):
    try:
        await HotelsService(db).delete_hotel(hotel_id)
        return {"status": "OK"}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
