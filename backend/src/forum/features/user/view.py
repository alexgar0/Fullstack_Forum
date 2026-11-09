from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from forum.core.config import settings
from forum.features.user.dependencies import UserServiceDep
from forum.features.user.schemas import Token, UserCreate, UserDTO
from forum.features.user.security import create_access_token, create_refresh_token
from forum.features.user.session import (
    get_current_user_for_activity,
    get_current_user_from_refresh_token,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserDTO, dependencies=[])
async def me(
    current_user: Annotated[UserDTO, Depends(get_current_user_for_activity)],
) -> UserDTO:
    return current_user


@router.post("/register", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, user_service: UserServiceDep) -> UserDTO:
    return user_service.create_user(user)


@router.post("/login", response_model=None)
async def login(
    user_service: UserServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> JSONResponse:
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
        max_age=settings.refresh_token_expire_minutes * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.refresh_token_expire_minutes * 60,
    )

    return response


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    current_user: Annotated[UserDTO, Depends(get_current_user_from_refresh_token)],
) -> Token:
    access_token = create_access_token(data={"sub": current_user.username})
    return Token(access_token=access_token, refresh_token="", token_type="bearer")  # noqa: S106


@router.get(
    "/{user_id}",
    response_model=UserDTO,
    dependencies=[Depends(get_current_user_for_activity)],
)
async def read_user(
    user_id: int,
    user_service: UserServiceDep,
) -> UserDTO:
    return user_service.view_user(user_id)


@router.post("/logout")
async def logout(response: Response) -> dict[str, str]:
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"status": "success"}
