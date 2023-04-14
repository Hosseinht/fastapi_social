from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    # schema
    # validate data with pydandic
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime

    class Config:
        orm_mode = True
