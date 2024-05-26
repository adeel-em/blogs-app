from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserInDB
from app.crud.user import get_user_by_username, update_user, deactivate_user
from app.api import deps

router = APIRouter()

@router.put("/{username}", response_model=UserInDB)
def update_user_by_username(username: str, user_update: UserCreate, db: Session = Depends(deps.get_db)):
    """
    Update user by username.
    """
    
    updated_user = update_user(db, username, user_update)
    return updated_user


@router.get("/{username}", response_model=UserInDB)
def read_user_by_username(username: str, db: Session = Depends(deps.get_db)):
    """
    Get user by username.
    """
    return get_user_by_username(db, username=username)
    
@router.delete("/{username}", response_model=UserInDB)
def delete_user_by_username(username: str, db: Session = Depends(deps.get_db)):
    """
    Deactivate user by username.
    """
    user = deactivate_user(db, username)
    return user