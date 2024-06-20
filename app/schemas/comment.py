from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    blog_id: int


class CommentUpdate(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    content: str

    class Config:
        from_attributes = True


class CommentInDB(Comment):
    pass


class CommentWithPagination(BaseModel):
    data: list[Comment]
    total: int
    page: int
    limit: int
