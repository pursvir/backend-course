from pydantic import BaseModel
from src.schemas.hotels import Hotel
from sqlalchemy import select, insert, update, delete

class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self._session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self._session.execute(query)
        return [self.schema.model_validate(row) for row in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self._session.execute(query)
        row = result.scalars().one_or_none()
        if not row:
            return None
        return self.schema.model_validate(row)

    async def add(self, data: BaseModel):
        add_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self._session.execute(add_stmt)
        row = result.scalars().one()
        return self.schema.model_validate(row)

    async def edit(self, data: BaseModel, partially_updated: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=partially_updated))
        )
        await self._session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        await self._session.execute(delete_stmt)
