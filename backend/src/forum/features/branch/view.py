from typing import Annotated

from fastapi import APIRouter, Depends

from forum.features.branch.dependencies import BranchServiceDep
from forum.features.branch.schemas import (
    BranchCreateDTO,
    BranchDTO,
    BranchWithSmallTopicsDTO,
)
from forum.features.query import PaginationQuery
from forum.features.user.database.models import User
from forum.features.user.session import get_current_user

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get(
    "/", response_model=list[BranchDTO], dependencies=[Depends(get_current_user)]
)
async def read_all_branches(
    branch_service: BranchServiceDep,
) -> list[BranchDTO]:
    return branch_service.get_all_branches()


@router.get("/{branch_id}", response_model=BranchWithSmallTopicsDTO)
async def read_branch(
    branch_id: int,
    pagination: Annotated[PaginationQuery, Depends(PaginationQuery)],
    current_user: Annotated[User, Depends(get_current_user)],
    branch_service: BranchServiceDep,
) -> BranchWithSmallTopicsDTO:
    return branch_service.get_branch_with_small_topics(
        current_user, branch_id, pagination
    )


@router.post("/", response_model=BranchDTO, status_code=201)
async def create_branch(
    branch: BranchCreateDTO,
    current_user: Annotated[User, Depends(get_current_user)],
    branch_service: BranchServiceDep,
) -> BranchDTO:
    return branch_service.create_branch(current_user, branch)


@router.delete("/{branch_id}", status_code=204)
async def delete_branch(
    branch_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    branch_service: BranchServiceDep,
) -> None:
    branch_service.delete_branch(current_user, branch_id)
