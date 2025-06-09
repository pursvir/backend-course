from pydantic import BaseModel, Field, ConfigDict

class RoomBase(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int

class RoomRequestAdd(RoomBase):
    facilities_ids: list[int] | None = None

class RoomAdd(RoomBase):
    hotel_id: int

class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None

class RoomPatch(RoomPatchRequest):
    hotel_id: int | None = None
