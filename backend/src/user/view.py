from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .database.service import UserService
from .schemas import Token, UserCreate, User
from .security import (
    create_access_token,
    create_refresh_token
)
from .session import get_current_user, get_current_user_for_activity, get_current_user_from_refresh_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    new_user = user_service.create_user(user)
    return new_user


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user_service = UserService(db)
    user = user_service.authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    user_service.update_last_login(user.id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    current_user: User = Depends(get_current_user_from_refresh_token),
):
    access_token = create_access_token(data={"sub": current_user.username})
    return {
        "access_token": access_token,
        "refresh_token": "", # Or return the same refresh token
        "token_type": "bearer",
    }


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user_for_activity)):
    return current_user