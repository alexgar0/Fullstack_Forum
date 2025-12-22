from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ...topic.database.models import Topic
from ...exceptions import ExistingResourceError, NotFoundError

from .models import Branch


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
            if 'branches_title' in str(e.orig):
                raise ExistingResourceError("Branch with the same title already exists")
            if "branches_parent_id" in str(e.orig):
                raise NotFoundError("Parent branch not found")
            raise
    
    def get_branch(self, branch_id: int) -> Branch:
        branch = self.db.query(Branch).filter(Branch.id == branch_id).first()
        if not branch:
            raise NotFoundError("Branch not found")
        return branch
    
    def update_branch(self, branch: Branch) -> Branch:
        self.db.add(branch)
        self.db.commit()
        self.db.refresh(branch)
        return branch
    
    def get_topics_by_branch_id(self, branch_id: int) -> list[Topic]:
        exists = self.db.query(
            self.db.query(Branch).filter(Branch.id == branch_id).exists()
        ).scalar()
        if not exists:
            raise NotFoundError("Branch not found")

        return (
            self.db.query(Topic)
            .filter(Topic.branch_id == branch_id)
            .all()
        )