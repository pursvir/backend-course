from httpx import AsyncClient


async def test_get_facilities(ac: AsyncClient):
    response = await ac.get(
        "/facilities",
    )
    print(f"ВОТ ОН ЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯ {type(response)=}")
    assert response.status_code == 200
    # assert isinstance(response.json(), list)


async def test_add_facilities(ac: AsyncClient):
    facility_title = "Кондиционер"
    response = await ac.post("/facilities", json={"title": facility_title})
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["data"]["title"] == facility_title
