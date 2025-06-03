from pydantic import BaseModel, Field, ConfigDict

class RoomRequestAdd(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int

class RoomAdd(RoomRequestAdd):
    hotel_id: int

class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class RoomPatchRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)

class RoomPatch(RoomPatchRequest):
    hotel_id: int | None = Field(None)
