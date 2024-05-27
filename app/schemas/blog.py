from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    content: str
    tags: str


class BlogCreate(BlogBase):
    owner_id: int


class BlogUpdate(BlogBase):
    is_published: bool


class Blog(BlogBase):
    id: int
    owner_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class BlogInDB(Blog):
    pass


class BlogWithPagination(BaseModel):
    data: list[Blog]
    total: int
    page: int
    limit: int
