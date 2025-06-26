from pydantic import BaseModel, Field, ConfigDict

from src.schemas.facilities import Facility

class RoomBase(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int

class RoomRequestAdd(RoomBase):
    facilities_ids: list[int] = []

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
