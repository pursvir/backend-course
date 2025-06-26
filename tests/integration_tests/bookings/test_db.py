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
    await db.bookings.add(booking_data)

    added_booking = (await db.bookings.get_one_or_none())
    assert added_booking
    assert added_booking.user_id == user_id
    assert added_booking.room_id == room_id
    assert added_booking.date_from == date_from
    assert added_booking.date_to == date_to
    assert added_booking.price == 100

    date_from = date(year=2025, month=5, day=10)
    date_to = date(year=2025, month=6, day=15)
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
        price=150,
    )
    await db.bookings.edit(booking_data, id=1)
    added_booking = (await db.bookings.get_one_or_none())
    assert added_booking
    assert added_booking.user_id == user_id
    assert added_booking.room_id == room_id
    assert added_booking.date_from == date_from
    assert added_booking.date_to == date_to
    assert added_booking.price == 150

    await db.bookings.delete(id=1)
    added_booking = (await db.bookings.get_one_or_none())
    assert not added_booking

    await db.commit()
