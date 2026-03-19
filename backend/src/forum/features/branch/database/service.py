from typing import Generator, List, Optional
from fastapi import Depends
from forum.features.query import PaginationQuery
from forum.features.topic.database.service import TopicService
from sqlalchemy.orm import Session


from forum.config import settings

from forum.database import get_db
from forum.exceptions import AppException, NotFoundError, PermissionDeniedError

from forum.features.user.database.models import Role, User

from forum.features.branch.database.repo import BranchRepo
from forum.features.branch.database.models import Branch
from forum.features.branch.schemas import BranchDTO, BranchCreateDTO, BranchWithSmallTopicsDTO


class WrongBranchTitleLength(AppException):
    def __init__(
        self,
        message: str = f"Branch title must be beetween {settings.branch_name_length_bounds[0]} and {settings.branch_name_length_bounds[1]} characters long",
    ) -> None:
        super().__init__(message)


class BranchService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo: BranchRepo = BranchRepo(db)

    def get_branch(self, user: User, branch_id: int) -> BranchDTO:
        branch = self.repo.get_by_id(branch_id)
        if not branch:
            raise NotFoundError("Branch not found")

        if user.role != Role.admin and not branch.is_active:
            raise PermissionDeniedError(message="Branch is not active")
        self.repo.increment_views(branch_id)
        return BranchDTO.model_validate(branch)

    def get_branch_with_small_topics(self, user: User, branch_id: int, pagination: Optional[PaginationQuery] = None) -> BranchWithSmallTopicsDTO:
        branch = self.get_branch(user, branch_id)
        topic_service = TopicService(self.db)
        pagination_result = topic_service.get_small_topics_from_branch_with_pagination(
            branch_id, pagination
        )
        base_dto = BranchDTO.model_validate(branch)
        return BranchWithSmallTopicsDTO(**base_dto.model_dump(), small_topics=list(pagination_result.items), pagination=pagination_result.to_dto())
    
    def get_all_branches(self) -> List[BranchDTO]:
        result = []
        orm_branches = self.repo.get_all()
        for orm_branch in orm_branches:
            result.append(BranchDTO.model_validate(orm_branch))
        return result

    def create_branch(self, user: User, branch: BranchCreateDTO) -> BranchDTO:
        print(branch)
        if not user.is_admin:
            raise PermissionDeniedError("Only admin can create a branch")

        if (
            len(branch.title) < settings.branch_name_length_bounds[0]
            or len(branch.title) > settings.branch_name_length_bounds[1]
        ):
            raise WrongBranchTitleLength

        new_branch = Branch(**branch.model_dump(), creator=user)
        orm_branch = self.repo.create(new_branch)
        return BranchDTO.model_validate(orm_branch)

    def delete_branch(self, user: User, branch_id: int) -> None:
        if not user.is_admin:
            raise PermissionDeniedError("Only admin can delete the branch")

        updated_branch = self.repo.update(entity_id=branch_id, is_active=False)
        if not updated_branch:
            raise NotFoundError("Branch not found")


def get_branch_service(
    db: Session = Depends(get_db),
) -> Generator[BranchService, None, None]:
    try:
        branch_service = BranchService(db)
        yield branch_service
    finally:
        pass
