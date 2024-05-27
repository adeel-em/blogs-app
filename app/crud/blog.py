from sqlalchemy.orm import Session
from app.models.user import User
from app.models.blog import Blog
from app.schemas.blog import BlogCreate, BlogUpdate
from fastapi import HTTPException
from app.core.constants import UserRole


def get_blog(db: Session, blog_id: int) -> Blog:
    """
    Get a blog by id.
    """

    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


def get_blogs(
    db: Session,
    page: int = 1,
    limit: int = 10,
    search: str = None,
    is_published: bool = None,
    created_from: str = None,
    created_to: str = None,
    author_id: int = None,
):
    """
    Get all blogs.
    """

    query = db.query(Blog)

    if search:
        query = query.filter(Blog.tags.ilike(f"%{search}%"))

    if is_published is not None:
        query = query.filter(Blog.is_published == is_published)

    if created_from:
        query = query.filter(Blog.created_at >= created_from)

    if created_to:
        query = query.filter(Blog.created_at <= created_to)

    if author_id:
        query = query.filter(Blog.owner_id == author_id)

    total = query.count()
    data = query.offset((page - 1) * limit).limit(limit).all()

    return {"data": data, "total": total, "page": page, "limit": limit}


def get_blogs_by_owner_id(db: Session, owner_id: int):
    """
    Get all blogs by owner id.
    """
    blog = db.query(Blog).filter(Blog.owner_id == owner_id).all()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


def get_blog_by_owner_id(db: Session, blog_id: int, owner_id: int):
    """
    Get a blog by owner id.
    """

    blog = db.query(Blog).filter(Blog.id == blog_id, Blog.owner_id == owner_id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


def create_blog(db: Session, blog: BlogCreate) -> Blog:
    """
    Create a new blog.
    """
    db_blog = Blog(title=blog.title, content=blog.content, owner_id=blog.owner_id)
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


def delete_blog(db: Session, blog_id: int, current_user: User):
    """
    Delete a blog.
    """
    if current_user.role == UserRole.ADMIN:
        db_blog = get_blog(db, blog_id)
    else:
        db_blog = get_blog_by_owner_id(db, blog_id, current_user.id)

    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    db.delete(db_blog)
    db.commit()
    return db_blog
