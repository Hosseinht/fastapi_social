from datetime import datetime

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    # schema
    # validate data with pydandic
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
