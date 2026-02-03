from typing import Generator, List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ..query import PaginationQuery
from ..user.database.models import User
from ..user.session import get_current_user, get_current_user_for_activity

from .database.service import BranchService, get_branch_service
from .schemas import BranchDTO, BranchCreateDTO, BranchWithSmallTopicsDTO

from ..topic.database.service import TopicService, get_topic_service

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("/", response_model=List[BranchDTO])
async def read_all_branches(
    current_user: User = Depends(get_current_user),
    branch_service: BranchService = Depends(get_branch_service)
):
    return branch_service.get_all_branches()


@router.get("/{branch_id}", response_model=BranchWithSmallTopicsDTO)
async def read_branch(
    branch_id: int,
    pagination: PaginationQuery = Depends(PaginationQuery),
    current_user: User = Depends(get_current_user),
    branch_service: BranchService = Depends(get_branch_service),
    topic_service: TopicService = Depends(get_topic_service)
):
    branch = branch_service.get_branch(current_user, branch_id)
    small_topics = topic_service.get_small_topics_from_branch_with_pagination(branch_id, pagination)
    base_dto = BranchDTO.model_validate(branch)
    dto = BranchWithSmallTopicsDTO(
        **base_dto.model_dump(), 
        small_topics=small_topics
    )
    return dto


@router.post("/", response_model=BranchDTO, status_code=201)
async def create_branch(
    branch: BranchCreateDTO,
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
