from datetime import timedelta, datetime, timezone
from typing import List
from sqlalchemy.orm import Session

from ...exceptions import NotFoundError, PermissionDeniedError

from ...user.database.models import User

from .repo import BranchRepo
from ..schemas import Branch
from ..schemas import BranchCreate

class BranchService:
    def __init__(self, db: Session) -> None:
        self.repo = BranchRepo(db)
        
    def get_branch(self, branch_id: int) -> Branch:
        return self.repo.get_branch(branch_id)
    
    def get_all_branches(self) -> List[Branch]:
        return self.repo.get_all_branches()
        
    def create_branch(self, user: User, branch: BranchCreate) -> Branch:
        if not user.is_admin:
            raise PermissionDeniedError("Only admin can create a branch")
        
        new_branch = Branch(**branch.model_dump(), creator_id=user.id)
        return self.repo.create_branch(new_branch)
    
    def delete_branch(self, user: User, branch_id: int) -> None:
        branch = self.repo.get_branch(branch_id)
        
        if not user.is_admin:
            raise PermissionDeniedError("Only admin can delete the branch")
        
        branch.is_active = False
        self.repo.update_branch(branch)