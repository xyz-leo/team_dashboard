from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Creates a new user with hashed password.
    
    Args:
        db: Database session
        user_data: User creation data
        
    Returns:
        User: Newly created user
        
    Raises:
        HTTPException: If user creation fails
    """
    try:
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user instance
        new_user = User(
            username=user_data.username,
            email=user_data.email,
        )
        
        # Hash and set password using model method
        new_user.set_password(user_data.password)
        
        # Save to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


def get_all_users(db: Session) -> list[User]:
    """
    Retrieve all users from database.
    
    Args:
        db: Database session
        
    Returns:
        list[User]: List of all users
    """
    try:
        return db.query(User).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving users: {str(e)}"
        )


def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Retrieve a user by ID.
    
    Args:
        db: Database session
        user_id: ID of the user to retrieve
        
    Returns:
        User: Requested user
        
    Raises:
        HTTPException: If user not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    """
    Update user information.
    
    Args:
        db: Database session
        user_id: ID of the user to update
        user_data: Data to update
        
    Returns:
        User: Updated user
        
    Raises:
        HTTPException: If user not found or update fails
    """
    try:
        # Find user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields if provided
        update_data = user_data.model_dump(exclude_unset=True)
        
        if "username" in update_data and update_data["username"]:
            # Check if new username is taken by another user
            existing_user = db.query(User).filter(
                User.username == update_data["username"],
                User.id != user_id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
            user.username = update_data["username"]
        
        if "email" in update_data and update_data["email"]:
            # Check if new email is taken by another user
            existing_email = db.query(User).filter(
                User.email == update_data["email"],
                User.id != user_id
            ).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            user.email = update_data["email"]
        
        if "password" in update_data and update_data["password"]:
            user.set_password(update_data["password"])
        
        # Commit changes
        db.commit()
        db.refresh(user)
        
        return user
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )


def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user by ID.
    
    Args:
        db: Database session
        user_id: ID of the user to delete
        
    Returns:
        bool: True if deletion was successful
        
    Raises:
        HTTPException: If user not found or deletion fails
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        db.delete(user)
        db.commit()
        
        return True
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )


def get_user_by_email(db: Session, email: str) -> User:
    """
    Retrieve a user by email address.
    
    Args:
        db: Database session
        email: Email address to search for
        
    Returns:
        User: User with matching email, or None if not found
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User:
    """
    Retrieve a user by username.
    
    Args:
        db: Database session
        username: Username to search for
        
    Returns:
        User: User with matching username, or None if not found
    """
    return db.query(User).filter(User.username == username).first()
