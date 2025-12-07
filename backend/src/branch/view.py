from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..user.database.models import User
from ..user.session import get_current_user, get_current_user_for_activity

from .database.service import BranchService
from .schemas import Branch, BranchCreate


router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("/{branch_id}", response_model=Branch)
async def read_branches(branch_id: int, current_user: User = Depends(get_current_user_for_activity), db: Session = Depends(get_db)):
    branch_service = BranchService(db)
    branch = branch_service.get_branch(branch_id)
    return branch


@router.post("/", response_model=Branch, status_code=201)
async def create_branch(branch: BranchCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    branch_service = BranchService(db)
    new_branch = branch_service.create_branch(current_user, branch)
    return new_branch


@router.delete("/{branch_id}", status_code=204)
async def delete_branch(branch_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    branch_service = BranchService(db)
    branch_service.delete_branch(current_user, branch_id)
