from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship, backref
from app.db.session import Base
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(2000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True, default=None)

    owner = relationship("User", back_populates="comments")
    blog = relationship("Blog", back_populates="comments")
    replies = relationship("Comment", backref=backref("parent", remote_side=[id]))
