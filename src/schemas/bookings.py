from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.fields import pos_int


class BookingAddRequest(BaseModel):
    room_id: pos_int
    date_from: date
    date_to: date


class BookingAdd(BookingAddRequest):
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
