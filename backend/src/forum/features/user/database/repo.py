from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from forum.core.exceptions import ExistingResourceError
from forum.features.common.repo import CRUDRepo, ViewableRepo
from forum.features.user.database.models import User


class UserRepo(CRUDRepo[User], ViewableRepo[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def create(self, entity: User) -> User:
        try:
            return super().create(entity)
        except IntegrityError as exc:
            self.db.rollback()
            if "users_email" in str(exc.orig):
                raise ExistingResourceError("Email already registered") from exc
            if "users_username" in str(exc.orig):
                raise ExistingResourceError("Username already taken") from exc
            raise

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()
