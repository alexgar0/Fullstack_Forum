from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from forum.features.topic.database.models import Topic
from forum.exceptions import ExistingResourceError, NotFoundError

from forum.features.branch.database.models import Branch


class BranchRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_branch(self, branch: Branch) -> Branch:
        try:
            self.db.add(branch)
            self.db.commit()
            self.db.refresh(branch)
            return branch
        except IntegrityError as e:
            self.db.rollback()
            if "branches_title" in str(e.orig):
                raise ExistingResourceError("Branch with the same title already exists")
            if "branches_parent_id" in str(e.orig):
                raise NotFoundError("Parent branch not found")
            raise

    def get_branch(self, branch_id: int) -> Branch:
        branch = self.db.query(Branch).filter(Branch.id == branch_id).first()
        if not branch:
            raise NotFoundError("Branch not found")
        return branch

    def get_all_branches(self) -> List[Branch]:
        branches = self.db.query(Branch).all()
        return branches

    def update_branch(self, branch: Branch) -> Branch:
        self.db.add(branch)
        self.db.commit()
        self.db.refresh(branch)
        return branch

    def get_topics(self, branch: Branch) -> List[Topic]:
        return self.db.query(Topic).filter(Topic.branch_id == branch.id).all()

    
