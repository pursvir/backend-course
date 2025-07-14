from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing import Annotated, List

from sqlalchemy.ext.asyncio.session import async_session

from src.db import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token")
    if access_token is None:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return access_token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    user_id = data["user_id"]
    return user_id


UserIDDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
