from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from forum.database import get_db
from forum.features.user.database.service import UserService
from forum.features.user.schemas import Token, UserCreate, User
from forum.features.user.security import create_access_token, create_refresh_token
from forum.features.user.session import (
    get_current_user,
    get_current_user_for_activity,
    get_current_user_from_refresh_token,
)
from forum import config


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=User)
async def me(current_user: User = Depends(get_current_user_for_activity)):
    return current_user


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    new_user = user_service.create_user(user)
    return new_user


@router.post("/login", response_model=Token)
async def login(
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

    response = JSONResponse({"status": "success"})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=config.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=config.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )

    return response


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    current_user: User = Depends(get_current_user_from_refresh_token),
):
    access_token = create_access_token(data={"sub": current_user.username})
    return {
        "access_token": access_token,
        "refresh_token": "",  # Or return the same refresh token
        "token_type": "bearer",
    }


@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    current_user: User = Depends(get_current_user_for_activity),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"status": "success"}
