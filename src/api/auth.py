from fastapi import APIRouter
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from src.repos.users import UsersRepository
from src.db import async_session_maker
from src.schemas.users import UserAdd, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(data: UserRequestAdd):
    password_hash = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, password_hash=password_hash)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
        except IntegrityError:
            return {"status": "NOT OK: user exists!"}
    return {"status": "OK"}


# @router.post("/login")

# @router.post("/logout")
