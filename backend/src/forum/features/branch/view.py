from typing import List
from fastapi import APIRouter, Depends

from forum.features.query import PaginationQuery
from forum.features.user.database.models import User
from forum.features.user.session import get_current_user

from forum.features.branch.database.service import BranchService, get_branch_service
from forum.features.branch.schemas import (
    BranchDTO,
    BranchCreateDTO,
    BranchWithSmallTopicsDTO,
)

from forum.features.topic.database.service import TopicService, get_topic_service

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("/", response_model=List[BranchDTO])
async def read_all_branches(
    current_user: User = Depends(get_current_user),
    branch_service: BranchService = Depends(get_branch_service),
) -> List[BranchDTO]:
    return branch_service.get_all_branches()


@router.get("/{branch_id}", response_model=BranchWithSmallTopicsDTO)
async def read_branch(
    branch_id: int,
    pagination: PaginationQuery = Depends(PaginationQuery),
    current_user: User = Depends(get_current_user),
    branch_service: BranchService = Depends(get_branch_service),
    topic_service: TopicService = Depends(get_topic_service),
) -> BranchWithSmallTopicsDTO:
    dto = branch_service.get_branch_with_small_topics(current_user, branch_id, pagination)
    return dto


@router.post("/", response_model=BranchDTO, status_code=201)
async def create_branch(
    branch: BranchCreateDTO,
    current_user: User = Depends(get_current_user),
    branch_service: BranchService = Depends(get_branch_service),
) -> BranchDTO:
    new_branch = branch_service.create_branch(current_user, branch)
    return new_branch


@router.delete("/{branch_id}", status_code=204)
async def delete_branch(
    branch_id: int,
    current_user: User = Depends(get_current_user),
    branch_service: BranchService = Depends(get_branch_service),
) -> None:
    branch_service.delete_branch(current_user, branch_id)
