from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.schemas.blog import BlogCreate, BlogUpdate, Blog, BlogInDB, BlogWithPagination
from app.crud.blog import create_blog, get_blog, get_blogs, update_blog, delete_blog
from app.api.deps import get_db, all_roles, admin_and_author, author_only
from app.limiter import limiter
from app.core.redis import RedisClient
import json


router = APIRouter()


@router.post("/", response_model=BlogInDB)
@limiter.limit("100/minute")
def create_blog_endpoint(
    request: Request,
    blog_in: BlogCreate,
    db: Session = Depends(get_db),
    current_user: BlogInDB = Depends(author_only),
):
    """
    Create a new blog.
    """
    return create_blog(db, blog_in, author=current_user)


@router.put("/{blog_id}", response_model=BlogInDB)
@limiter.limit("100/minute")
def update_blog_endpoint(
    request: Request,
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
@limiter.limit("100/minute")
def read_blog(
    request: Request,
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: BlogInDB = Depends(all_roles),
):
    """
    Get blog by id.
    """

    blog = get_blog(db, blog_id=blog_id)
    return blog


@router.get("/", response_model=BlogWithPagination)
@limiter.limit("100/minute")
async def read_blogs(
    request: Request,
    page: int = 1,
    limit: int = 10,
    search: str = None,
    is_published: bool = None,
    created_from: str = None,
    created_to: str = None,
    author_id: int = None,
    db: Session = Depends(get_db),
    current_user: BlogInDB = Depends(all_roles),
):
    """
    Get all blogs.
    """

    try:
        redis_client = await RedisClient.get_instance()
        cashe_key = f"blogs_{page}_{limit}_{search}_{is_published}_{created_from}_{created_to}_{author_id}"

        # try to get data from redis
        cashed_data = await redis_client.get(cashe_key)
        if cashed_data:
            return json.loads(cashed_data)

        data = get_blogs(
            db, page, limit, search, is_published, created_from, created_to, author_id
        )

        # save data to redis
        # redis_instance = await redis_client
        # await result.set(cashe_key, json.dumps(data.to_dict()))

        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{blog_id}", response_model=BlogInDB)
@limiter.limit("100/minute")
def delete_blog_endpoint(
    request: Request,
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: BlogInDB = Depends(admin_and_author),
):
    """
    Delete blog by id.
    """
    return delete_blog(db, blog_id, current_user)
