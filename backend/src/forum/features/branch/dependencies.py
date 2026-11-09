from typing import Annotated

from fastapi import Depends

from forum.features.branch.service import BranchService, get_branch_service

BranchServiceDep = Annotated[BranchService, Depends(get_branch_service)]
