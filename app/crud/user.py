from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException





def get_user(db: Session, user_id: int) -> User:
    """
    Get a user by id.
    """
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    Get all users.
    """
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_username(db: Session, username: str) -> User:
    """
    Get a user by username.
    """
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> User:
    """
    Get a user by email.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user.
    """
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, username: str, user: UserUpdate) -> User:
    """
    Update a user.
    """

    db_user = get_user_by_username(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

def deactivate_user(db: Session, username: str) -> User:
    """
    Deactivate a user by setting is_active to False.
    """

    user = get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user = db.query(User).filter(User.username == username).first()
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user