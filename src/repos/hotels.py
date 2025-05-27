from src.repos.base import BaseRepository
from src.models.hotels import HotelsORM
from sqlalchemy import select, insert, func

class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(
        self,
        location: str,
        title: str,
        limit: int,
        offset: int,
    ):
        query = select(HotelsORM)
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self._session.execute(query)
        return result.scalars().all()

    # async def get_one_or_none(self, **filter_by):
    #     ...

    async def add(self, title, location):
        stmt = (
            insert(HotelsORM)
            .values(title=title, location=location)
            .returning(HotelsORM)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()[0]
