from typing import List
from forum.features.common.repo import CRUDRepo, OwnableRepo, ViewableRepo
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from forum.features.topic.database.models import Topic
from forum.exceptions import ExistingResourceError, NotFoundError

from forum.features.branch.database.models import Branch


class BranchRepo(CRUDRepo[Branch], ViewableRepo[Branch], OwnableRepo[Branch]):
    def __init__(self, db: Session):
        super().__init__(db, Branch)

    def create(self, entity: Branch) -> Branch:
        try:
            return super().create(entity)
        except IntegrityError as e:
            self.db.rollback()
            if "branches_title" in str(e.orig):
                raise ExistingResourceError("Branch with the same title already exists")
            if "branches_parent_id" in str(e.orig):
                raise NotFoundError("Parent branch not found")
            raise
