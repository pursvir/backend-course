from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from src.config import settings
from src.exceptions import (
    IncorrectPasswordException,
    NonValidTokenException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.schemas.users import UserAdd, UserAddRequest
from src.services.base import BaseService


class CryptoService:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            raise NonValidTokenException

    def hash_password(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)


class AuthService(BaseService):
    async def add_user(self, user_data: UserAddRequest) -> None:
        password_hash = CryptoService().hash_password(user_data.password)
        new_user_data = UserAdd(email=user_data.email, password_hash=password_hash)
        try:
            await self.db.users.add(new_user_data)
        except ObjectAlreadyExistsException:
            raise UserAlreadyExistsException
        await self.db.commit()

    async def get_access_token_for_user(self, data: UserAddRequest):
        user = await self.db.users.get_user_with_hashed_password(
            email=data.email,
        )
        if not user:
            raise UserNotFoundException
        if not CryptoService().verify_password(data.password, user.password_hash):
            raise IncorrectPasswordException
        return CryptoService().create_access_token({"user_id": user.id})

    async def get_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)
