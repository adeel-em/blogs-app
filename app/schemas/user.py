from pydantic import BaseModel, EmailStr
from enum import Enum


class RoleEnum(Enum):
    reader = "reader"
    admin = "admin"
    author = "author"


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    role: RoleEnum

    class Config:
        use_enum_values = True


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreateUpdate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserInDB(User):
    pass


class UserInResponse(User):
    token: str


class UserWithPagination(BaseModel):
    data: list[User]
    total: int
    page: int
    limit: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenRequest(BaseModel):
    username: str
    password: str
