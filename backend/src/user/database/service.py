from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .repo import UserRepo
from ..schemas import UserCreate
from ..security import hash_password
from .models import User
from ..security import verify_password

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

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepo(db)
        
    def create_user(self, user: UserCreate) -> User:
        pwd_check = password_complexity_check(user.password)
        if not pwd_check[0]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=pwd_check[1])
        
        db_user_by_email = self.repo.get_user_by_email(user.email)
        if db_user_by_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        db_user_by_username = self.repo.get_user_by_username(user.username)
        if db_user_by_username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
        
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
    
    
    def update_user_role(self, user_id, role) -> User:
        user = self.repo.get_user(user_id)
        user.role = role
        self.repo.db.add(user)
        self.repo.db.commit()
        self.repo.db.refresh(user)
        return user

    def update_last_activity(self, user_id) -> User:
        user = self.repo.get_user(user_id)
        user.last_activity = datetime.now()
        return user
    
    def update_last_login(self, user_id) -> User:
        user = self.repo.get_user(user_id)
        user.last_login = datetime.now()
        user.last_activity = datetime.now()
        self.repo.db.add(user)
        self.repo.db.commit()
        self.repo.db.refresh(user)
        return user