from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentInDB,
    CommentWithPagination,
)
from app.limiter import limiter
from app.crud.comment import (
    create_comment,
    get_comment,
    get_comments,
    update_comment,
    delete_comment,
)
from app.api.deps import (
    get_db,
    all_roles,
    reader_only,
    admin_and_reader,
)
from app.core.config import settings

router = APIRouter()


@router.post("/", response_model=CommentInDB)
@limiter.limit(f"{settings.MAX_REQUESTS_COUNT}/minute")
def create_comment_endpoint(
    request: Request,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: CommentInDB = Depends(reader_only),
):
    """
    Create a new comment.
    """
    return create_comment(db, comment_in, current_user)


@router.put("/{comment_id}", response_model=CommentInDB)
@limiter.limit(f"{settings.MAX_REQUESTS_COUNT}/minute")
def update_comment_endpoint(
    request: Request,
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: CommentInDB = Depends(reader_only),
):
    """
    Update comment by id.
    """
    updated_comment = update_comment(db, comment_id, comment_update, current_user)
    return updated_comment


@router.get("/{comment_id}", response_model=CommentInDB)
@limiter.limit(f"{settings.MAX_REQUESTS_COUNT}/minute")
def read_comment(
    request: Request,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: CommentInDB = Depends(all_roles),
):
    """
    Get comment by id.
    """

    comment = get_comment(db, comment_id=comment_id)
    return comment


@router.get("/", response_model=CommentWithPagination)
@limiter.limit(f"{settings.MAX_REQUESTS_COUNT}/minute")
def read_comments(
    request: Request,
    page: int = 1,
    limit: int = 10,
    blog_id: int = 0,
    db: Session = Depends(get_db),
    current_user: CommentInDB = Depends(all_roles),
):
    """
    Get all comments.
    """
    return get_comments(db, page, limit, blog_id)


@router.delete("/{comment_id}", response_model=CommentInDB)
@limiter.limit(f"{settings.MAX_REQUESTS_COUNT}/minute")
def delete_comment_endpoint(
    request: Request,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: CommentInDB = Depends(admin_and_reader),
):
    """
    Delete comment by id.
    """
    return delete_comment(db, comment_id, current_user)
