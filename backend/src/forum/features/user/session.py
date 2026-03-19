from fastapi import Depends, HTTPException, Request, status
from jose import JWTError
import jwt
from sqlalchemy.orm import Session

from forum.config import settings
from forum.database import get_db
from forum.features.user.database.service import UserService
from forum.features.user.database.models import User


def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if token.startswith("Bearer "):
        token = token[7:]
    return token


def get_current_user(
    token: str = Depends(get_token_from_cookie), db: Session = Depends(get_db)
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
    except JWTError:
        raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_service = UserService(db)
    user = user_service.repo.get_user_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user


def get_current_user_for_activity(
    token: str = Depends(get_token_from_cookie), db: Session = Depends(get_db)
) -> User:
    user = get_current_user(token=token, db=db)
    user_service = UserService(db)
    user_service.update_last_activity(user.id)
    return user


def get_current_user_from_refresh_token(
    token: str = Depends(get_token_from_cookie), db: Session = Depends(get_db)
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
    except JWTError:
        raise credentials_exception

    user_service = UserService(db)
    user = user_service.repo.get_user_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user
