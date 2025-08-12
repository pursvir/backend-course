from pydantic import BaseModel, ConfigDict

from src.schemas.fields import str_not_null


class FacilityAdd(BaseModel):
    title: str_not_null


class Facility(FacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
