from pydantic import BaseModel
from typing import Optional


class BlogBase(BaseModel):
    title: str
    content: str
    tags: str


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BlogBase):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
    is_published: Optional[bool] = None


class Blog(BlogBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class BlogInDB(Blog):
    pass


class BlogWithPagination(BaseModel):
    data: list[Blog]
    total: int
    page: int
    limit: int
