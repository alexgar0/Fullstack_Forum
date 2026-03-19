from typing import Any, Dict, Generator, List, cast
from fastapi import Depends
from forum.features.topic.database.models import Topic
from sqlalchemy.orm import Query, Session


from forum.config import settings

from forum.database import get_db
from forum.exceptions import AppException, NotFoundError, PermissionDeniedError

from forum.features.user.database.models import Role, User

from forum.features.branch.database.repo import BranchRepo
from forum.features.branch.database.models import Branch
from forum.features.branch.schemas import BranchDTO, BranchCreateDTO


class WrongBranchTitleLength(AppException):
    def __init__(
        self,
        message: str = f"Branch title must be beetween {settings.branch_name_length_bounds[0]} and {settings.branch_name_length_bounds[1]} characters long",
    ) -> None:
        super().__init__(message)


class BranchService:
    def __init__(self, db: Session) -> None:
        self.repo: BranchRepo = BranchRepo(db)

    def _branch_to_dto(self, branch: Branch) -> Dict[str, Any]:
        return {
            "id": branch.id,
            "title": branch.title,
            "description": branch.description,
            "creator_id": branch.creator_id,
            "is_active": branch.is_active,
            "created_at": branch.created_at,
            "parent_id": branch.parent_id,
            "topic_count": cast(Query[Topic], branch.topics).count(),
            "children_ids": [c.id for c in branch.children],
        }

    def get_branch(self, user: User, branch_id: int) -> BranchDTO:
        branch = self.repo.get_by_id(branch_id)
        if not branch:
            raise NotFoundError("Branch not found")
        
        if user.role != Role.admin and not branch.is_active:
            raise PermissionDeniedError(message="Branch is not active")
        data = self._branch_to_dto(branch)
        return BranchDTO.model_validate(data)

    def get_all_branches(self) -> List[BranchDTO]:
        result = []
        orm_branches = self.repo.get_all()
        for orm_branch in orm_branches:
            data = self._branch_to_dto(orm_branch)
            result.append(BranchDTO.model_validate(data))
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
        data = self._branch_to_dto(orm_branch)
        return BranchDTO.model_validate(data)

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
