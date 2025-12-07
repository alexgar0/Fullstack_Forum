from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ...exceptions import ExistingResourceError

from .models import User


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError as e:
            self.db.rollback()
            if 'users_email' in str(e.orig):
                raise ExistingResourceError("Email already registered")
            if 'users_username' in str(e.orig):
                raise ExistingResourceError("Username already taken")
            raise

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def update_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user