from pydantic import BaseModel, EmailStr, ConfigDict


class UserAddRequest(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    password_hash: str


class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    password_hash: str
