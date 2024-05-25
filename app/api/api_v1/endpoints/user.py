from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.schemas.user import UserCreate, UserInDB
from app.crud.user import create_user
from app.api import deps

router = APIRouter()

# @router.get("/", response_model=schemas.UserCreate)
# def read_user_me(current_user: models.User = Depends(deps.get_current_user)):
#     """
#     Get the current user.
#     """
#     return current_user

@router.post("/", response_model=UserInDB)
def create_user_endpoint(user_in:  UserCreate, db: Session = Depends(deps.get_db)):
    """
    Create a new user.
    """
    user_exist = crud.user.get_user_by_username(db, username=user_in.username)
    if user_exist:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    user = crud.user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user_in)

@router.put("/profile/{username}", response_model=UserInDB)
def update_user_by_username(username: str, user_update: UserCreate, db: Session = Depends(deps.get_db)):
    """
    Update user by username.
    """
    
    updated_user = crud.user.update_user(db, username, user_update)
    return updated_user


@router.get("/profile/{username}", response_model=UserInDB)
def read_user_by_username(username: str, db: Session = Depends(deps.get_db)):
    """
    Get user by username.
    """

    user = crud.user.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User deactivated")
    
    return user
@router.delete("/profile/{username}", response_model=UserInDB)
def delete_user_by_username(username: str, db: Session = Depends(deps.get_db)):
    """
    Deactivate user by username.
    """
    user = crud.user.deactivate_user(db, username)
    return user