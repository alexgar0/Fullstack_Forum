from collections.abc import Generator
from typing import Annotated

from fastapi import Depends

from forum.features.branch.service import BranchService
from forum.features.common.dependencies import DatabaseDep


def get_branch_service(
    db: DatabaseDep,
) -> Generator[BranchService]:
    try:
        branch_service = BranchService(db)
        yield branch_service
    finally:
        pass


BranchServiceDep = Annotated[BranchService, Depends(get_branch_service)]
