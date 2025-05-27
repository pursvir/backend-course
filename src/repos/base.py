from sqlalchemy import select, insert
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
        return result.scalars.one_or_none()

    async def add(self, *args, **kwargs):
        stmt = insert(self.model).values(**kwargs)
        result = await self._session.execute(stmt)
        return result
