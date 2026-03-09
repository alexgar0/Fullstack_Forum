from datetime import timedelta, datetime, timezone
from typing import Generator, List
from fastapi import Depends
from sqlalchemy.orm import Session


from forum.config import BRANCH_NAME_LENGTH_BOUNDS

from forum.database import get_db
from forum.exceptions import AppException, NotFoundError, PermissionDeniedError

from forum.features.user.database.models import Role, User
from forum.features.query import PaginationQuery

from forum.features.branch.database.repo import BranchRepo
from forum.features.branch.database.models import Branch
from forum.features.branch.schemas import BranchDTO, BranchCreateDTO


class WrongBranchTitleLength(AppException):
    def __init__(
        self,
        message: str = f"Branch title must be beetween {BRANCH_NAME_LENGTH_BOUNDS[0]} and {BRANCH_NAME_LENGTH_BOUNDS[1]} characters long",
    ) -> None:
        super().__init__(message)


class BranchService:
    def __init__(self, db: Session) -> None:
        self.repo: BranchRepo = BranchRepo(db)

    def get_branch(self, user: User, branch_id: int) -> BranchDTO:
        branch = self.repo.get_branch(branch_id)
        if user.role != Role.admin and not branch.is_active:
            raise PermissionDeniedError(message="Branch is not active")
        return BranchDTO.model_validate(branch)

    def get_all_branches(self) -> List[BranchDTO]:
        result = []
        orm_branches = self.repo.get_all_branches()
        for orm_branch in orm_branches:
            result.append(BranchDTO.model_validate(orm_branch))
        return result

    def create_branch(self, user: User, branch: BranchCreateDTO) -> BranchDTO:
        print(branch)
        if not user.is_admin:
            raise PermissionDeniedError("Only admin can create a branch")

        if (
            len(branch.title) < BRANCH_NAME_LENGTH_BOUNDS[0]
            or len(branch.title) > BRANCH_NAME_LENGTH_BOUNDS[1]
        ):
            raise WrongBranchTitleLength

        new_branch = Branch(**branch.model_dump(), is_active=True, creator_id=user.id)
        orm_branch = self.repo.create_branch(new_branch)
        return BranchDTO.model_validate(orm_branch)

    def delete_branch(self, user: User, branch_id: int) -> None:
        branch = self.repo.get_branch(branch_id)

        if not user.is_admin:
            raise PermissionDeniedError("Only admin can delete the branch")

        branch.is_active = False
        self.repo.update_branch(branch)


def get_branch_service(
    db: Session = Depends(get_db),
) -> Generator[BranchService, None, None]:
    try:
        branch_service = BranchService(db)
        yield branch_service
    finally:
        pass
