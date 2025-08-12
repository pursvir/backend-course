from pydantic import BaseModel, ConfigDict

from src.schemas.fields import str_not_null


class HotelAdd(BaseModel):
    title: str_not_null
    location: str_not_null


class Hotel(HotelAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class HotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None
