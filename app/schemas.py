from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Schema is a data structure that defines the expected format of the data. it is used to validate data before it is
# stored or processed.
class PostBase(BaseModel):
    # schema
    # validate data with pydandic
    title: str
    content: str
    published: bool = True


class PostCreateSchema(PostBase):
    pass


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserOutSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostOutSchema(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    user_id: int
    user: "UserOutSchema"
    created_at: datetime

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    id: Optional[str] = None
