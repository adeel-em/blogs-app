from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Enum as EnumColumn
from sqlalchemy.orm import relationship
from app.db.session import Base
from sqlalchemy import Boolean
from enum import Enum


class UserRole(Enum):
    reader = "reader"
    admin = "admin"
    author = "author"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(1000))
    is_active = Column(Boolean, default=True)
    role = Column(EnumColumn(UserRole), default=UserRole.reader)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    blogs = relationship("Blog", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")

    @classmethod
    async def get_by_email(cls, db_session, email: str):
        return db_session.query(cls).filter(cls.email == email).first()
