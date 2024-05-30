from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserInDB, UserInResponse, UserLogin
from app.crud.user import create_user, login_user
from app.api import deps
from app.limiter import limiter

router = APIRouter()


@router.post("/register", response_model=UserInDB)
@limiter.limit("50/minute")
def register_user_endpoint(
    request: Request, user_in: UserCreate, db: Session = Depends(deps.get_db)
):
    """
    Register a new user.
    """
    return create_user(db, user_in)


@router.post("/login", response_model=UserInResponse)
@limiter.limit("5/minute")
def login_user_endpoint(
    request: Request, user_in: UserLogin, db: Session = Depends(deps.get_db)
):
    """
    Login a user.
    """
    user = login_user(db, user_in.username, user_in.password)

    response = Response()

    response.set_cookie(key="auth_token", value=user.token, max_age=7200, httponly=True)

    response.status_code = 200
    response.data = {"user": user, "access_token": user.token, "token_type": "bearer"}
    return response