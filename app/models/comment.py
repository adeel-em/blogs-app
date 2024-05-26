from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base
from sqlalchemy import Boolean

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(Integer, index=True)
    blog_id = Column(Integer, index=True)

    owner = relationship("User", back_populates="comments")
    blog = relationship("Blog", back_populates="comments")
    
    # This is a class method that