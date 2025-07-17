from typing import Type, TypeVar

from pydantic.main import BaseModel
from sqlalchemy import Row, RowMapping

from src.db import Base

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: Type[Base]
    schema: Type[SchemaType]  # type: ignore

    def __init__(self) -> None:
        pass

    @classmethod
    def map_to_domain_entity(cls, data: Base | dict | Row | RowMapping):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: BaseModel):
        return cls.db_model(**data.model_dump())
