from typing import Sequence
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from src.db import Base
from src.repos.mappers.base import DataMapper


class BaseRepository:
    model: Base = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [ self.mapper.map_to_domain_entity(row) for row in result.scalars().all() ]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        row = result.scalars().one_or_none()
        if not row:
            return None
        return self.mapper.map_to_domain_entity(row)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        row = result.scalars().one()
        return self.mapper.map_to_domain_entity(row)

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        row = result.scalars().one()
        return self.mapper.map_to_domain_entity(row)

    async def add_bulk(self, data: Sequence[BaseModel]) -> None:
        add_data_stmt = (
            insert(self.model)
            .values([item.model_dump() for item in data])
        )
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, partially_updated: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=partially_updated))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        await self.session.execute(delete_stmt)
