from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.blog import BlogCreate, BlogUpdate, Blog, BlogInDB
from app.crud.blog import create_blog, get_blog, get_blogs, update_blog, delete_blog
from app.api.deps import get_db, all_roles, admin_and_author, author_only


router = APIRouter()


@router.post("/", response_model=BlogInDB)
def create_blog_endpoint(
    blog_in: BlogCreate,
    db: Session = Depends(get_db),
    current_user: BlogInDB = Depends(author_only),
):
    """
    Create a new blog.
    """
    return create_blog(db, blog_in)


@router.put("/{blog_id}", response_model=BlogInDB)
def update_blog_endpoint(
    blog_id: int,
    blog_update: BlogUpdate,
    db: Session = Depends(get_db),
    current_user: BlogInDB = Depends(author_only),
):
    """
    Update blog by id.
    """
    updated_blog = update_blog(db, blog_id, blog_update)
    return updated_blog


@router.get("/{blog_id}", response_model=BlogInDB)
def read_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: BlogInDB = Depends(all_roles),
):
    """
    Get blog by id.
    """

    blog = get_blog(db, blog_id=blog_id)
    return blog


@router.get("/", response_model=list[BlogInDB])
def read_blogs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: BlogInDB = Depends(all_roles),
):
    """
    Get all blogs.
    """
    return get_blogs(db, skip, limit)


@router.delete("/{blog_id}", response_model=BlogInDB)
def delete_blog_endpoint(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: BlogInDB = Depends(admin_and_author),
):
    """
    Delete blog by id.
    """
    return delete_blog(db, blog_id, current_user)
