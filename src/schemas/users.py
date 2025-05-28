from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str

class UserAdd(BaseModel):
    email: EmailStr
    password_hash: str

class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
