from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.repos.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility, RoomFacility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User, UserWithHashedPassword


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel


class RoomsDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Room


class RoomsFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesORM
    schema = RoomFacility


class RoomsWithRelsDataMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomWithRels


class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = Booking


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facility


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User


class UserWithHashedPasswordDataMapper(DataMapper):
    db_model = UsersORM
    schema = UserWithHashedPassword
