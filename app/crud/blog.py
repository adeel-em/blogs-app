from sqlalchemy.orm import Session
from app.models.user import User
from app.models.blog import Blog
from app.schemas.blog import BlogCreate, BlogUpdate
from fastapi import HTTPException


def get_blog(db: Session, blog_id: int) -> Blog:
    """
    Get a blog by id.
    """

    
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    return blog


def get_blogs(db: Session, skip: int = 0, limit: int = 10):
    """
    Get all blogs.
    """
    return db.query(Blog).offset(skip).limit(limit).all()

def get_blogs_by_owner_id(db: Session, owner_id: int):
    """
    Get all blogs by owner id.
    """
    blog = db.query(Blog).filter(Blog.owner_id == owner_id).all()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    return blog

def create_blog(db: Session, blog: BlogCreate) -> Blog:
    """
    Create a new blog.
    """
    db_blog = Blog(
        title=blog.title,
        content=blog.content,
        owner_id=blog.owner_id
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def update_blog(db: Session, blog_id: int, blog: BlogUpdate) -> Blog:
    """
    Update a blog.
    """

    db_blog = get_blog(db, blog_id=blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    db_blog.title = blog.title
    db_blog.content = blog.content
    db_blog.is_published = blog.is_published
    db.commit()
    db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int):
    """
    Delete a blog.
    """
    db_blog = get_blog(db, blog_id=blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    db.delete(db_blog)
    db.commit()
    return db_blog