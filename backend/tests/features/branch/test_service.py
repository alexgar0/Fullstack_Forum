from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from forum.core.config import settings
from forum.core.exceptions import NotFoundError, PermissionDeniedError
from forum.features.branch.schemas import BranchCreateDTO
from forum.features.branch.service import BranchService, WrongBranchTitleLengthError
from forum.features.user.models import Role


@pytest.fixture
def service():
    service = BranchService(Mock())
    service.repo = Mock()
    return service


def test_create_branch_rejects_non_admin(service):
    user = SimpleNamespace(is_admin=False)
    with pytest.raises(PermissionDeniedError):
        service.create_branch(user, BranchCreateDTO(title="Valid title"))
    service.repo.create.assert_not_called()


@pytest.mark.parametrize(
    "length",
    (
        settings.branch_name_length_bounds[0] - 1,
        settings.branch_name_length_bounds[1] + 1,
    ),
)
def test_create_branch_rejects_invalid_title_length(service, length):
    with pytest.raises(WrongBranchTitleLengthError):
        service.create_branch(
            SimpleNamespace(is_admin=True), BranchCreateDTO(title="x" * length)
        )
    service.repo.create.assert_not_called()


def test_get_missing_branch_does_not_increment_views(service):
    service.repo.get_by_id.return_value = None
    with pytest.raises(NotFoundError):
        service.get_branch(SimpleNamespace(role=Role.user), 1)
    service.repo.increment_views.assert_not_called()


def test_get_inactive_branch_denied_to_user(service):
    service.repo.get_by_id.return_value = SimpleNamespace(is_active=False)
    with pytest.raises(PermissionDeniedError):
        service.get_branch(SimpleNamespace(role=Role.user), 1)
    service.repo.increment_views.assert_not_called()


def test_delete_missing_branch(service):
    service.repo.update.return_value = None
    with pytest.raises(NotFoundError):
        service.delete_branch(SimpleNamespace(is_admin=True), 1)
    service.repo.update.assert_called_once_with(entity_id=1, is_active=False)
