from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate, CommentUpdate, CommentInDB
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

router = APIRouter()


@router.post("/", response_model=CommentInDB)
@limiter.limit("100/minute")
def create_comment_endpoint(
    request: Request,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: CommentInDB = Depends(reader_only),
):
    """
    Create a new comment.
    """
    return create_comment(db, comment_in)


@router.put("/{comment_id}", response_model=CommentInDB)
@limiter.limit("100/minute")
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
    updated_comment = update_comment(db, comment_id, comment_update)
    return updated_comment


@router.get("/{comment_id}", response_model=CommentInDB)
@limiter.limit("100/minute")
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


@router.get("/", response_model=list[CommentInDB])
@limiter.limit("100/minute")
def read_comments(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: CommentInDB = Depends(all_roles),
):
    """
    Get all comments.
    """
    return get_comments(db, skip, limit)


@router.delete("/{comment_id}", response_model=CommentInDB)
@limiter.limit("100/minute")
def delete_comment_endpoint(
    request: Request,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: CommentInDB = Depends(admin_and_reader),
):
    """
    Delete comment by id.
    """
    return delete_comment(db, comment_id)
