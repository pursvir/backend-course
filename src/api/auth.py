import aboba
from fastapi import APIRouter, Response

from src.api.dependencies import DBDep, UserIDDep
from src.exceptions import (
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    UserAlreadyExistsHTTPException,
    UserNotFoundHTTPException,
)
from src.schemas.users import UserAddRequest
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(db: DBDep, user_data: UserAddRequest):
    try:
        await AuthService(db).add_user(user_data)
    except ObjectAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(db: DBDep, user_data: UserAddRequest, response: Response):
    try:
        token = await AuthService(db).get_access_token_for_user(user_data)
    except ObjectNotFoundException:
        raise UserNotFoundHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", token)
    return {"access_token": token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIDDep):
    return await AuthService(db).get_user(user_id)


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
