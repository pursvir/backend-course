from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from src.models.hotels import HotelsORM

class BaseRepository:
    model = None

    def __init__(self, session):
        self._session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self._session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self._session.execute(add_stmt)
        return result.scalars.one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump())
        )
        await self._session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        await self._session.execute(delete_stmt)
