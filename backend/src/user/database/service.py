from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from ...exceptions import AppException, ExistingResourceError, PermissionDeniedError
from ..schemas import UserCreate
from ..security import hash_password, verify_password
from .models import User, Role
from .repo import UserRepo

from ...config import USERNAME_LENGTH_BOUNDS

def password_complexity_check(password) -> tuple[bool, str]:
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
        
class WrongUsernameLength(AppException):
    def __init__(self, message: str = f"Username length must be beetween {USERNAME_LENGTH_BOUNDS[0]} and {USERNAME_LENGTH_BOUNDS[1]} characters long"):
        super().__init__(message, status_code=422)

class EmailAlreadyRegistered(ExistingResourceError):
    def __init__(self, message: str = f"Email is already registered"):
        super().__init__(message)
        
class UsernameAlreadyTaken(ExistingResourceError):
    def __init__(self, message: str = f"Username is already taken"):
        super().__init__(message)

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepo(db)
        
    def get_user(self, user_id: int) -> User:
        return self.repo.get_user_by_id(user_id)
        
    def create_user(self, user: UserCreate) -> User:
        if len(user.username) < USERNAME_LENGTH_BOUNDS[0] or len(user.username) > USERNAME_LENGTH_BOUNDS[1]:
            raise WrongUsernameLength()
        
        pwd_check = password_complexity_check(user.password)
        if not pwd_check[0]:
            raise PasswordTooWeakError(pwd_check[1])
        
        if self.repo.get_user_by_email(user.email):
            raise EmailAlreadyRegistered()
        
        if self.repo.get_user_by_username(user.username):
            raise UsernameAlreadyTaken()
        
        hashed_pass = hash_password(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_pass
        )
        return self.repo.create_user(db_user)
    
    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.repo.get_user_by_username(username)
        if not user:
            user = self.repo.get_user_by_email(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    
    def update_user_role(self, initiator_user: User, user_to_update: User, role: Role) -> User:
        if not initiator_user.is_admin:
            raise PermissionDeniedError("You are not an admin")
        user_to_update.role = role
        self.repo.update_user(user_to_update)
        return user_to_update

    def update_last_activity(self, user_id) -> User:
        user = self.repo.get_user_by_id(user_id)
        user.last_activity = datetime.now()
        self.repo.update_user(user)
        return user
    
    def update_last_login(self, user_id) -> User:
        user = self.repo.get_user_by_id(user_id)
        user.last_login = datetime.now()
        self.repo.update_user(user)
        return user