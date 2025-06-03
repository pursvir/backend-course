# ...

from src.models.rooms import RoomsORM
from src.repos.base import BaseRepository
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room
