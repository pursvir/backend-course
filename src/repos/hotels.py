from src.repos.base import BaseRepository
from src.models.hotels import HotelsORM
from sqlalchemy import select, insert, delete, func

class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(
        self,
        location,
        title,
        limit,
        offset,
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
