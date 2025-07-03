import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.api.dependencies import get_db
from src.db import Base, engine_np, async_session_maker_np
from src.config import settings
from src.models import *
from src.repos.mappers.mappers import HotelDataMapper, RoomsDataMapper
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"

async def get_db_np():
    async with DBManager(async_session_maker_np) as db:
        yield db

@pytest.fixture(scope="function")
async def db():
    async for db in get_db_np():
        yield db

app.dependency_overrides[get_db] = get_db_np

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_np.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session", autouse=True)
async def fill_database(setup_database):
    with open("tests/mock_hotels.json", encoding="utf-8") as hotels_file,\
         open("tests/mock_rooms.json", encoding="utf-8") as rooms_file:
        hotels = json.load(hotels_file)
        rooms = json.load(rooms_file)
    hotels_data = [ HotelAdd.model_validate(hotel, from_attributes=True) for hotel in hotels ]
    rooms_data = [ RoomAdd.model_validate(room, from_attributes=True) for room in rooms ]

    async with DBManager(async_session_maker_np) as db_:
        await db_.hotels.add_bulk(hotels_data)
        await db_.rooms.add_bulk(rooms_data)
        await db_.commit()

auth_credentials = {
    "email": "gusev@gmail.com",
    "password": "12345678",
}

@pytest.fixture(scope="session", autouse=True)
async def register_user(fill_database, ac):
    await ac.post(
        "/auth/register",
        json=auth_credentials
    )

@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    await ac.post(
        "/auth/login",
        json=auth_credentials
    )
    assert ac.cookies["access_token"]
    yield ac
