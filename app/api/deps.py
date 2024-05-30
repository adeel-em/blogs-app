from typing import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.crud.user import get_user_by_username
from jose import JWTError
from app.models.user import User
from starlette.status import HTTP_401_UNAUTHORIZED
from app.core.constants import UserRole


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    Yields a new session and ensures it is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    alowed_roles: list[UserRole] = [],
) -> User:
    """
    Dependency that returns the current user from the database.
    """

    try:
        if not token:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="No authorization header"
            )

        payload = decode_access_token(token)

        if payload is None:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
            )

        username: str = payload.get("username")
        if username is None:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
        )

    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        if user.role.value not in alowed_roles:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=f"Not enough permissions",
            )
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def admin_and_author(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    return get_current_user(db, token, [UserRole.ADMIN, UserRole.AUTHOR])


def admin_and_reader(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    return get_current_user(db, token, [UserRole.ADMIN, UserRole.READER])


def all_roles(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    return get_current_user(
        db, token, [UserRole.ADMIN, UserRole.AUTHOR, UserRole.READER]
    )


def admin_only(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    return get_current_user(db, token, [UserRole.ADMIN])


def author_only(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    return get_current_user(db, token, [UserRole.AUTHOR])


def reader_only(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    return get_current_user(db, token, [UserRole.READER])
