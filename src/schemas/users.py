from pydantic import BaseModel, ConfigDict, EmailStr

from src.schemas.fields import str_not_null


class UserAddRequest(BaseModel):
    email: EmailStr
    password: str_not_null


class UserAdd(BaseModel):
    email: EmailStr
    password_hash: str


class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    password_hash: str
