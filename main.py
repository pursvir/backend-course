from fastapi import FastAPI, Request, Query, Body
import uvicorn

app = FastAPI(docs_url=None)

hotels = [
    {"id": 1, "title": "Sochi", "name": "Sochi"},
    {"id": 2, "title": "Дубай", "name": "Dubai"},
]

@app.get("/hotels")
def get_hotels(
    # or Optional[type] (typing.Optional) on older Python
    id: int | None = Query(description="Hotel ID in the database"),
    title: str | None = Query(description="Hotel name"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
           continue
        hotels_.append(hotel)
    return hotels_

@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True, description="Hotel name")
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}

# НАЧАЛО МОЕГО КОДА
@app.put("/hotels/{hotel_id}")
def put_hotel(
    hotel_id: int,
    title: str = Body(description="Hotel title"),
    name: str= Body(description="Hotel name")
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
    return {"status": "NOT OK"}

@app.patch("/hotels/{hotel_id}")
def patch_hotel(
    hotel_id: int,
    title: str | None = Body(description="Hotel title"),
    name: str | None = Body(description="Hotel name")
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
            return {"status": "OK"}
    return {"status": "NOT OK"}
# КОНЕЦ МОЕГО КОДА

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
