from src.models.rooms import RoomsORM
from src.repos.base import BaseRepository

class RoomsRepository(BaseRepository):
    model = RoomsORM
    # ...
