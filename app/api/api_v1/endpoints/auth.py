from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserInDB
from app.crud.user import create_user, get_user_by_username, get_user_by_email
from app.api import deps

router = APIRouter()

@router.post("/register", response_model=UserInDB)
def register_user_endpoint(user_in:  UserCreate, db: Session = Depends(deps.get_db)):
    """
    Register a new user.
    """
    return create_user(db, user_in)

@router.post("/login", response_model=UserInDB)
def login_user_endpoint(user_in:  UserCreate, db: Session = Depends(deps.get_db)):
    """
    Login a user.
    """
    return get_user_by_username(db, username=user_in.username)