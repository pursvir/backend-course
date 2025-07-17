from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersORM
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        row = result.scalars().one_or_none()
        if row is None:
            return None
        return UserWithHashedPassword.model_validate(row)
