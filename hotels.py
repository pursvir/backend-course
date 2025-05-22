from fastapi import Query, Path, Body, APIRouter
from schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

PER_PAGE_DEFAULT = 4

@router.get(
    "",
    summary="Получение отелей",
    description="<h3>Тут мы можем запросить данные об отелях в базе. В query опционально можно указать ID, title, name.\
    Также поддерживается пагинация, где page - порядковый номер страницы, а per_page - сколько вы хотите получить отелей в ответе</h3>"
)
def get_hotels(
    # or Optional[type] (typing.Optional) on older Python
    id: int | None = Query(None, description="Hotel ID in the database"),
    title: str | None = Query(None, description="Hotel name"),
    page: int | None = Query(None, description="Page sequence number"),
    per_page: int | None = Query(None, description="Hotels per page count"),
):
    if (page and page < 1) or (per_page and per_page < 1):
        # Тут по идее нужно отсылать клиенту что-то из диапазона 400, но мы пока не дошли до этого :)
        return []
    if not page:
        page = 1
    if not per_page:
        per_page = PER_PAGE_DEFAULT
    begin_index = (page - 1) * per_page
    hotels_ = []
    for hotel in hotels[begin_index:(begin_index + per_page)]:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
           continue
        hotels_.append(hotel)
    return hotels_

@router.post(
    "",
    summary="Добавление отеля",
    description="<h3>Тут мы добавляем новый отель: нужно отправить name и title</h3>"
)
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звёзд у моря",
        "name": "sochi_u_morya",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай 5 звёзд у фонтана",
        "name": "dubai_fontane",
    }},
})):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status": "OK"}

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
