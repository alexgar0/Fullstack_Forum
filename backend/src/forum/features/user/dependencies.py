from typing import Annotated

from fastapi import Depends

from forum.features.common.dependencies import DatabaseDep
from forum.features.user.service.service import UserService


def get_user_service(db: DatabaseDep) -> UserService:
    return UserService(db)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
