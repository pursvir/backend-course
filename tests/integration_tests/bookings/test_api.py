import pytest
from httpx import AsyncClient

from tests.conftest import authenticated_ac

room_booking_params = [
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 400),
]

successful_room_bookings = 0

@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    room_booking_params
)
async def test_add_bookings(
    room_id: int, date_from: str, date_to: str, status_code: int,
    db, authenticated_ac: AsyncClient,
):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    res = response.json()
    assert isinstance(res, dict)
    if status_code == 200:
        assert res["status"] == "OK"
        assert "data" in res
        global successful_room_bookings
        successful_room_bookings += 1
        await get_bookings_count(authenticated_ac)

async def get_bookings_count(
    authenticated_ac: AsyncClient
):
    response = await authenticated_ac.get("/bookings/me")
    res = response.json()
    assert isinstance(res, list) # or list?
    assert len(res) == successful_room_bookings
