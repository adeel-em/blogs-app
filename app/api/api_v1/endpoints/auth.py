from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserInDB, UserInResponse, UserLogin
from app.crud.user import create_user, login_user
from app.api import deps

router = APIRouter()

@router.post("/register", response_model=UserInDB)
def register_user_endpoint(user_in:  UserCreate, db: Session = Depends(deps.get_db)):
    """
    Register a new user.
    """
    return create_user(db, user_in)

@router.post("/login", response_model=UserInResponse)
def login_user_endpoint(user_in:  UserLogin, db: Session = Depends(deps.get_db)):
    """
    Login a user.
    """
    return login_user(db, user_in.username, user_in.password)