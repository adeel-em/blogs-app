from fastapi import APIRouter, Depends, Response, Request, Form
from sqlalchemy.orm import Session
from app.schemas.user import (
    UserCreateUpdate,
    UserInDB,
    UserInResponse,
    UserLogin,
    TokenResponse,
    TokenRequest,
)
from app.crud.user import create_user, login_user
from app.api import deps
from app.limiter import limiter
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=UserInDB)
@limiter.limit(f"{settings.MAX_AUTH_REQUESTS_COUNT}/minute")
def register_user_endpoint(
    request: Request, user_in: UserCreateUpdate, db: Session = Depends(deps.get_db)
):
    """
    Register a new user.
    """
    return create_user(db, user_in)


@router.post("/login", response_model=UserInResponse)
@limiter.limit(f"{settings.MAX_AUTH_REQUESTS_COUNT}/minute")
def login_user_endpoint(
    request: Request, user_in: UserLogin, db: Session = Depends(deps.get_db)
):
    """
    Login a user.
    """
    user = login_user(db, user_in.username, user_in.password)
    response = Response()
    response.set_cookie(key="auth_token", value=user.token, max_age=7200, httponly=True)
    return user


@router.post("/token", response_model=TokenResponse)
async def get_token(
    request: Request,
    username=Form(...),
    password=Form(...),
    db: Session = Depends(deps.get_db),
):
    """
    Get token.
    """

    form_data = TokenRequest(username=username, password=password)
    user = login_user(db, form_data.username, form_data.password)
    return {"access_token": user.token, "token_type": "bearer"}
