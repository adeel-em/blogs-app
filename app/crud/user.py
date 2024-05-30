from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreateUpdate
from app.core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException


def get_user(db: Session, user_id: int) -> User:
    """
    Get a user by id.
    """
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    Get all users.
    """
    try:
        return db.query(User).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_user_by_username(db: Session, username: str) -> User:
    """
    Get a user by username.
    """

    try:
        return db.query(User).filter(User.username == username).first()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_user_by_email(db: Session, email: str) -> User:
    """
    Get a user by email.
    """

    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def create_user(db: Session, user_in: UserCreateUpdate) -> User:
    """
    Create a new user.
    """

    try:
        user_exist = get_user_by_username(db, username=user_in.username)
        if user_exist:
            raise HTTPException(status_code=400, detail="Username already registered")

        user = get_user_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user_in.password)

        db_user = User(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            username=user_in.username,
            email=user_in.email,
            role=user_in.role,
            password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def login_user(db: Session, username: str, password: str) -> User:
    """
    Login a user.
    """
    try:

        user = get_user_by_username(db, username=username)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        if not user.is_active:
            raise HTTPException(status_code=400, detail="User deactivated")

        user.token = create_access_token(data={"sub": user.username})

        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def update_user(db: Session, username: str, user: UserCreateUpdate) -> User:
    """
    Update a user.
    """

    try:
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def deactivate_user(db: Session, username: str) -> User:
    """
    Deactivate a user by setting is_active to False.
    """

    try:
        user = get_user_by_username(db, username=username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.is_active = False
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
