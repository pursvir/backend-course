import logging
from typing import Any, Sequence

from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Base
from src.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException
from src.repos.mappers.base import DataMapper


class BaseRepository:
    model: type[Base]
    mapper: type[DataMapper]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filter_by) -> list[BaseModel | Any]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(row) for row in result.scalars().all()]

    async def get_all(self, *args, **kwargs) -> list[BaseModel | Any]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by) -> BaseModel | None | Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        row = result.scalars().one_or_none()
        if not row:
            return None
        return self.mapper.map_to_domain_entity(row)

    async def get_one(self, **filter_by) -> BaseModel | None | Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            row = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(row)

    async def add(self, data: BaseModel) -> BaseModel | Any:
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_data_stmt)
            row = result.scalars().one()
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):  # type: ignore
                raise ObjectAlreadyExistsException
            else:
                logging.exception(f"Unknown error, failed to add following data: {data}")
                raise ex
        return self.mapper.map_to_domain_entity(row)

    async def add_bulk(self, data: Sequence[BaseModel]) -> None:
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, partially_updated: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=partially_updated))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
