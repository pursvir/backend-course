from fastapi import APIRouter, HTTPException, Response
from services.auth import AuthService
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import UserIDDep
from src.db import async_session_maker
from src.schemas.users import UserAdd, UserRequestAdd
from src.repos.users import UsersRepository
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(data: UserRequestAdd):
    password_hash = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, password_hash=password_hash)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
        except IntegrityError:
            raise HTTPException(status_code=401, detail="Пользователь с данным email уже существует!")
    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response):
    async with async_session_maker() as session:
        user = (
            await UsersRepository(session)
            .get_user_with_hashed_password(
                email=data.email,
            )
        )
        if not user:
            raise HTTPException(status_code=401, detail="Данного пользователя не существует!")
        if not AuthService().verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Пароль неверный!")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router.get("/me")
async def get_me(user_id: UserIDDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
