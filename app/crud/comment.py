from sqlalchemy.orm import Session
from app.models.user import User
from app.models.comment import Comment
from app.crud.blog import get_blog
from app.schemas.comment import CommentCreate, CommentUpdate
from fastapi import HTTPException
from app.core.constants import UserRole


def get_comment(db: Session, comment_id: int) -> Comment:
    """
    Get a comment by id.
    """
    try:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_comments(db: Session, page: int = 0, limit: int = 10, blog_id: int = 0):
    """
    Get all comments.
    """
    try:

        skip = (page - 1) * limit
        query = db.query(Comment)
        if blog_id != 0:
            query = query.filter(Comment.blog_id == blog_id)
        data = query.offset(skip).limit(limit).all()
        total = query.count()

        return {
            "data": data,
            "total": total,
            "page": page,
            "limit": limit,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_comments_by_blog_id(db: Session, blog_id: int):
    """
    Get all comments by blog id.
    """
    try:
        return db.query(Comment).filter(Comment.blog_id == blog_id).all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_comment_by_owner_id(db: Session, comment_id: int, owner_id: int):
    """
    Get a comment by owner id.
    """
    try:
        return (
            db.query(Comment)
            .filter(Comment.id == comment_id, Comment.owner_id == owner_id)
            .first()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def create_comment(db: Session, comment: CommentCreate, current_user: User) -> Comment:
    """
    Create a new comment.
    """
    try:

        blog = get_blog(db, comment.blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        db_comment = Comment(
            content=comment.content, owner_id=current_user.id, blog_id=comment.blog_id
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def update_comment(
    db: Session, comment_id: int, comment: CommentUpdate, current_user: User
) -> Comment:
    """
    Update a comment.
    """

    try:
        db_comment = get_comment_by_owner_id(
            db, comment_id=comment_id, owner_id=current_user.id
        )
        if not db_comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        db_comment.content = comment.content
        db.commit()
        db.refresh(db_comment)
        return db_comment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def delete_comment(db: Session, comment_id: int, current_user: User):
    """
    Delete a comment.
    """

    try:
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
