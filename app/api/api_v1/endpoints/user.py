from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserInDB
from app.crud.user import get_user_by_username, update_user, deactivate_user
from app.api.deps import get_db, all_roles

router = APIRouter()


@router.put("/{username}", response_model=UserInDB)
def update_user_by_username(
    user_update: UserCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(all_roles),
):
    """
    Update user by username.
    """

    updated_user = update_user(db, current_user.username, user_update)
    return updated_user


@router.get("/{username}", response_model=UserInDB)
def read_user_by_username(
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(all_roles),
):
    """
    Get user by username.
    """
    return get_user_by_username(db, current_user.username)


@router.delete("/{username}", response_model=UserInDB)
def delete_user_by_username(
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(all_roles),
):
    """
    Deactivate user by username.
    """
    user = deactivate_user(db, current_user.username)
    return user
