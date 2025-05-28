from src.models.users import UsersORM
from src.schemas.users import User
from src.repos.base import BaseRepository

class UsersRepository(BaseRepository):
    model = UsersORM
    schema = User
