from pydantic import BaseModel, ConfigDict
from datetime import date

class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class BookingAdd(BookingAddRequest):
    user_id: int
    price: int

class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
