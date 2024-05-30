from sqlalchemy.orm import Session
from app.models.user import User
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate
from fastapi import HTTPException
from app.core.constants import UserRole


def get_comment(db: Session, comment_id: int) -> Comment:
    """
    Get a comment by id.
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()


def get_comments(db: Session, skip: int = 0, limit: int = 10):
    """
    Get all comments.
    """
    return db.query(Comment).offset(skip).limit(limit).all()


def get_comments_by_blog_id(db: Session, blog_id: int):
    """
    Get all comments by blog id.
    """
    return db.query(Comment).filter(Comment.blog_id == blog_id).all()


def get_comment_by_owner_id(db: Session, comment_id: int, owner_id: int):
    """
    Get a comment by owner id.
    """
    return (
        db.query(Comment)
        .filter(Comment.id == comment_id, Comment.owner_id == owner_id)
        .first()
    )


def create_comment(db: Session, comment: CommentCreate) -> Comment:
    """
    Create a new comment.
    """
    db_comment = Comment(
        content=comment.content, owner_id=comment.owner_id, blog_id=comment.blog_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(db: Session, comment_id: int, comment: CommentUpdate) -> Comment:
    """
    Update a comment.
    """

    db_comment = get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db_comment.content = comment.content
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int, current_user: User):
    """
    Delete a comment.
    """

    if current_user.role == UserRole.ADMIN:
        db_comment = get_comment(db, comment_id)
    else:
        db_comment = get_comment_by_owner_id(db, comment_id, current_user.id)

    db_comment = get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(db_comment)
    db.commit()
    return db_comment
