from datetime import date
from sqlalchemy import select, func

from src.models.rooms import RoomsORM
from src.models.bookings import BookingsORM
from src.schemas import rooms

def room_ids_for_booking(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
):
    rooms_count = (
        select(BookingsORM.room_id, func.count('*').label("rooms_booked"))
        .select_from(BookingsORM)
        .filter(
            BookingsORM.date_from <= date_to,
            BookingsORM.date_to >= date_from
        ).
        group_by(BookingsORM.room_id)
        .cte(name="rooms_count")
    )
    rooms_left_table = (
        select(
            RoomsORM.id.label("room_id"),
            (RoomsORM.quantity - func.coalesce(
                rooms_count.c.rooms_booked, 0
            )).label("rooms_left")
        )
        .select_from(RoomsORM)
        .outerjoin(rooms_count, RoomsORM.id == rooms_count.c.room_id) # left join
        .cte(name="rooms_left_table")
    )
    room_ids_from_hotel = (
        select(RoomsORM.id)
        .select_from(RoomsORM)
    )
    if hotel_id is not None:
        room_ids_from_hotel = (
            room_ids_from_hotel.filter_by(hotel_id=hotel_id)
        )
    room_ids_from_hotel = (
        room_ids_from_hotel
        .subquery(name="room_ids_from_hotel")
    )
    query = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0,
            # TODO: causes SAWarning
            rooms_left_table.c.room_id.in_(room_ids_from_hotel), # type: ignore
        )
    )
    return query
