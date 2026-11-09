from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError

from forum.config import settings
from forum.features.user.database.models import User
from forum.features.user.dependencies import UserServiceDep


def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token.removeprefix("Bearer ")


def get_current_user(
    token: Annotated[str, Depends(get_token_from_cookie)], user_service: UserServiceDep
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        if payload.get("token_type") != "access":
            raise credentials_exception
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user = user_service.repo.get_user_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user


def get_current_user_for_activity(
    user: Annotated[User, Depends(get_current_user)], user_service: UserServiceDep
) -> User:
    user_service.update_last_activity(user.id)
    return user


def get_current_user_from_refresh_token(
    token: Annotated[str, Depends(get_token_from_cookie)], user_service: UserServiceDep
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials for refresh",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        if payload.get("token_type") != "refresh":
            raise credentials_exception
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = user_service.repo.get_user_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user
