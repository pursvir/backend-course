from fastapi import Query, Path, Body, APIRouter, Depends
from src.repos.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.db import async_session_maker
from src.schemas.hotels import Hotel, HotelPatch


router = APIRouter(prefix="/hotels", tags=["Отели"])

PER_PAGE_DEFAULT = 4

@router.get(
    "",
    summary="Получение отелей",
    description="<h3>Тут мы можем запросить данные об отелях в базе. В query опционально можно указать ID, title, name.\
    Также поддерживается пагинация, где page - порядковый номер страницы, а per_page - сколько вы хотите получить отелей в ответе</h3>"
)
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Hotel name"),
    location: str | None = Query(None, description="Hotel location")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location,
            title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

@router.post(
    "",
    summary="Добавление отеля",
    description="<h3>Тут мы добавляем новый отель: нужно отправить name и title</h3>"
)
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звёзд у моря",
        "location": "ул. Моря, 2",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай 5 звёзд у фонтана",
        "location": "ул. Шейха, 3",
    }},
})):
    async with async_session_maker() as session:
        new_hotel = await HotelsRepository(session).add(**hotel_data.model_dump())
        await session.commit()
    return {"status": "OK", "data": new_hotel}

@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных об отеле по ID",
    description="<h3>Тут мы полностью перезаписываем данные об отеле с указанным ID: можно отправить name, а можно title, а можно вообще ничего</h3>"
)
def put_hotel(
    hotel_id: int,
    hotel_data: Hotel,
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "OK"}
    return {"status": "NOT OK"}

@router.patch(
    "/hotels/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h3>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title, а можно вообще ничего</h3>"
)
def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPatch
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            return {"status": "OK"}
    return {"status": "NOT OK"}

@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля по ID",
    description="<h3>Отель, ID которого будет указан в path, будет удалён из базы</h3>"
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
