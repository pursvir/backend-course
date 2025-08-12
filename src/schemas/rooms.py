from pydantic import BaseModel, ConfigDict, field_validator

from src.schemas.facilities import Facility
from src.schemas.fields import str_not_null


class RoomBase(BaseModel):
    title: str_not_null
    description: str | None
    price: int
    quantity: int


class RoomRequestAdd(RoomBase):
    facilities_ids: list[int] = []

    @field_validator("facilities_ids")
    def check_ids(cls, facilities):
        if len(facilities) != len(set(facilities)):
            raise ValueError("ID удобств не могут повторяться")
        if not all(i > 0 for i in facilities):
            raise ValueError("Некорретный формат ID удобств")
        return facilities


class RoomAdd(RoomBase):
    hotel_id: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class RoomPatch(RoomPatchRequest):
    hotel_id: int | None = None
