from src.repos.base import BaseRepository
from src.repos.hotels import HotelsRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest

class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking
