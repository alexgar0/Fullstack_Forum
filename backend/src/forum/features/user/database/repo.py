from typing import Optional

from forum.features.common.repo import CRUDRepo
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from forum.exceptions import ExistingResourceError

from forum.features.user.database.models import User


class UserRepo(CRUDRepo[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def create(self, entity: User) -> User:
        try:
            return super().create(entity)
        except IntegrityError as e:
            self.db.rollback()
            if "users_email" in str(e.orig):
                raise ExistingResourceError("Email already registered")
            if "users_username" in str(e.orig):
                raise ExistingResourceError("Username already taken")
            raise

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
