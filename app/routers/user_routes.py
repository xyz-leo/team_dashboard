from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.services import user_service as UserService
from app.core.database import get_db

# APIRouter instance for user-related endpoints
router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.
    Uses UserService to handle business logic (e.g., password hashing).
    """
    user = UserService.create_user(db, user_data)
    return user


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve all users from the database.
    """
    users = UserService.get_all_users(db)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by its ID.
    Raises 404 if not found.
    """
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user's information by ID.
    """
    updated_user = UserService.update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by ID.
    """
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None

