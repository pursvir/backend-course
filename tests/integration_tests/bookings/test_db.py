from datetime import date

from src.db import async_session_maker_np
from src.schemas.bookings import BookingAdd
from src.utils.db_manager import DBManager


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    date_from = date(year=2025, month=4, day=5)
    date_to = date(year=2025, month=5, day=4)

    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
        price=100,
    )
    added_booking = await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(id=added_booking.id)
    assert booking
    assert booking.id == added_booking.id
    assert booking.model_dump(exclude={"id"}) == booking_data.model_dump()

    date_from = date(year=2025, month=5, day=10)
    date_to = date(year=2025, month=6, day=15)
    updated_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
        price=150,
    )
    await db.bookings.edit(updated_booking_data, id=added_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=added_booking.id)
    assert updated_booking
    assert (
        updated_booking.model_dump(exclude={"id"}) == updated_booking_data.model_dump()
    )

    await db.bookings.delete(id=added_booking.id)
    booking = await db.bookings.get_one_or_none(id=added_booking.id)
    assert not booking

    await db.rollback()
