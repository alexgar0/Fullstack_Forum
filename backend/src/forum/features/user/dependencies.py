from typing import Annotated

from fastapi import Depends

from forum.core.auth.session import get_current_user, get_current_user_for_activity
from forum.features.common.dependencies import DatabaseDep
from forum.features.user.database.models import User
from forum.features.user.service.service import UserService


def get_user_service(db: DatabaseDep) -> UserService:
    return UserService(db)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
ActivityCurrentUserDep = Annotated[User, Depends(get_current_user_for_activity)]
