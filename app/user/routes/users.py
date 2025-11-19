from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from shared.database.session import get_db
from app.user.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.user.auth.auth import create_access_token, get_current_user_username
from app.user.crud import user as crud_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """ Register a new user """
    user_exist = crud_user.get_user_by_username(db, user.username)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    email_exist = crud_user.get_user_by_email(db, user.email)
    if email_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        db_user = crud_user.create_user(db, user)
        return db_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
def login_user(form_data: UserLogin, db: Session = Depends(get_db)):
    """ Login user and return access token """
    user = crud_user.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_username: str = Depends(get_current_user_username), db: Session = Depends(get_db)):
    """ Get current user info """
    user = crud_user.get_user_by_username(db, current_username)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active"
        )
    return user

@router.delete("/{user_id}")
def delete_user_endpoint(user_id: int, current_username: str = Depends(get_current_user_username), db: Session = Depends(get_db)):
    """ Delete a user by ID (only admin or self) """
    success = crud_user.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}

@router.put("/{user_id}/deactivate")
def deactivate_user_endpoint(user_id: int, current_username: str = Depends(get_current_user_username), db: Session = Depends(get_db)):
    """ Deactivate a user by ID """
    user = crud_user.deactivate_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deactivated successfully", "user": user}

@router.put("/{user_id}/activate")
def activate_user_endpoint(user_id: int, current_username: str = Depends(get_current_user_username), db: Session = Depends(get_db)):
    """ Activate a user by ID """
    user = crud_user.activate_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User activated successfully", "user": user}