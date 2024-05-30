from pydantic import BaseModel


class CommentBase(BaseModel):
    blog_id: int
    owner_id: int


class CommentUpdate(CommentBase):
    content: str


class CommentCreate(CommentUpdate):
    pass


class Comment(CommentBase):
    id: int
    content: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class CommentInDB(Comment):
    pass
