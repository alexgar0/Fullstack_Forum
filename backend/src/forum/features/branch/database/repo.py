from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from forum.exceptions import ExistingResourceError, NotFoundError
from forum.features.branch.database.models import Branch
from forum.features.common.repo import CRUDRepo, OwnableRepo, ViewableRepo


class BranchRepo(CRUDRepo[Branch], ViewableRepo[Branch], OwnableRepo[Branch]):
    def __init__(self, db: Session):
        super().__init__(db, Branch)

    def create(self, entity: Branch) -> Branch:
        try:
            return super().create(entity)
        except IntegrityError as exc:
            self.db.rollback()
            if "branches_title" in str(exc.orig):
                raise ExistingResourceError(
                    "Branch with the same title already exists"
                ) from exc
            if "branches_parent_id" in str(exc.orig):
                raise NotFoundError("Parent branch not found") from exc
            raise
