from datetime import UTC, datetime

from sqlalchemy.orm import Session

from forum.core.auth.security import hash_password, verify_password
from forum.core.config import settings
from forum.core.exceptions import (
    AppException,
    ExistingResourceError,
    NotFoundError,
    PermissionDeniedError,
)
from forum.features.user.models import Role, User
from forum.features.user.repo import UserRepo
from forum.features.user.schemas import RegisterDTO, UserDTO


def password_complexity_check(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"


class PasswordTooWeakError(AppException):
    def __init__(self, message: str = "Password does not meet complexity requirements"):
        super().__init__(message, status_code=422)


class WrongUsernameLengthError(AppException):
    def __init__(
        self,
        message: str = f"Username length must be beetween {settings.username_length_bounds[0]} and {settings.username_length_bounds[1]} characters long",
    ):
        super().__init__(message, status_code=422)


class EmailAlreadyRegisteredError(ExistingResourceError):
    def __init__(self, message: str = "Email is already registered"):
        super().__init__(message)


class UsernameAlreadyTakenError(ExistingResourceError):
    def __init__(self, message: str = "Username is already taken"):
        super().__init__(message)


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepo(db)

    def get_user(self, user_id: int) -> UserDTO:
        orm_user = self.repo.get_by_id(user_id)
        return UserDTO.model_validate(orm_user)

    def view_user(self, user_id: int) -> UserDTO:
        self.repo.increment_views(user_id)
        return self.get_user(user_id)

    def create_user(self, user: RegisterDTO) -> UserDTO:
        if (
            len(user.username) < settings.username_length_bounds[0]
            or len(user.username) > settings.username_length_bounds[1]
        ):
            raise WrongUsernameLengthError

        pwd_check = password_complexity_check(user.password)
        if not pwd_check[0]:
            raise PasswordTooWeakError(pwd_check[1])

        if self.repo.get_user_by_email(user.email):
            raise EmailAlreadyRegisteredError

        if self.repo.get_user_by_username(user.username):
            raise UsernameAlreadyTakenError

        hashed_pass = hash_password(user.password)
        db_user = User(
            username=user.username,
            role=Role.user,
            email=user.email,
            hashed_password=hashed_pass,
        )
        orm_user = self.repo.create(db_user)
        return UserDTO.model_validate(orm_user)

    def authenticate_user(self, username: str, password: str) -> UserDTO | None:
        user = self.repo.get_user_by_username(username)
        if not user:
            user = self.repo.get_user_by_email(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return UserDTO.model_validate(user)

    def update_user_role(
        self, initiator_user: User, user_id: int, role: Role
    ) -> UserDTO:
        if not initiator_user.is_admin:
            raise PermissionDeniedError("You are not an admin")

        orm_user = self.repo.update(user_id, role=role)
        if not orm_user:
            raise NotFoundError("User not found")
        return UserDTO.model_validate(orm_user)

    def update_last_activity(self, user_id: int) -> UserDTO:
        now = datetime.now(tz=UTC)
        orm_user = self.repo.update(user_id, last_activity=now)
        if not orm_user:
            raise NotFoundError("User not found")
        return UserDTO.model_validate(orm_user)

    def update_last_login(self, user_id: int) -> UserDTO:
        now = datetime.now(tz=UTC)
        orm_user = self.repo.update(user_id, last_login=now)
        if not orm_user:
            raise NotFoundError("User not found")
        return UserDTO.model_validate(orm_user)
