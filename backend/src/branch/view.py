from typing import Generator, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..user.database.models import User
from ..user.session import get_current_user, get_current_user_for_activity

from .database.service import BranchService
from .schemas import Branch, BranchCreate


def get_branch_service(db: Session = Depends(get_db)) -> Generator[BranchService, None, None]:
    try:
        branch_service = BranchService(db)
        yield branch_service
    finally:
        pass


router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("/", response_class=List[Branch])
async def read_all_branches(
    current_user: User = Depends(get_current_user),
    branch_service: BranchService = Depends(get_branch_service)
):
    return branch_service.get_all_branches()


@router.get("/{branch_id}", response_model=Branch)
async def read_branch(
    branch_id: int,
    current_user: User = Depends(get_current_user),
    branch_service=Depends(get_branch_service)
):
    branch = branch_service.get_branch(branch_id)
    return branch


@router.post("/", response_model=Branch, status_code=201)
async def create_branch(
    branch: BranchCreate,
    current_user: User = Depends(get_current_user),
    branch_service: BranchService = Depends(get_branch_service)
):
    new_branch = branch_service.create_branch(current_user, branch)
    return new_branch


@router.delete("/{branch_id}", status_code=204)
async def delete_branch(
    branch_id: int,
    current_user: User = Depends(get_current_user),
    branch_service: BranchService = Depends(get_branch_service)
):
    branch_service.delete_branch(current_user, branch_id)
