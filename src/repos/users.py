from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersORM
from src.repos.mappers.mappers import UserDataMapper
from src.schemas.users import User, UserWithHashedPassword
from src.repos.base import BaseRepository

class UsersRepository(BaseRepository):
    model = UsersORM # type: ignore
    mapper = UserDataMapper # type: ignore

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email) # type: ignore
        result = await self.session.execute(query)
        row = result.scalars().one_or_none()
        if row is None:
            return None
        return UserWithHashedPassword.model_validate(row)
