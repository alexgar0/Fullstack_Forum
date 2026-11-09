from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from forum.core.config import settings
from forum.core.exceptions import (
    InvalidLengthError,
    NotFoundError,
    PermissionDeniedError,
)
from forum.features.topic.schemas import TopicCreateDTO, TopicUpdateDTO
from forum.features.topic.service import TopicService


@pytest.fixture
def service():
    service = TopicService(Mock())
    service.repo = Mock()
    return service


@pytest.mark.parametrize(
    "length",
    (
        settings.topic_title_length_bounds[0] - 1,
        settings.topic_title_length_bounds[1] + 1,
    ),
)
def test_create_topic_rejects_invalid_title(service, length):
    topic = TopicCreateDTO(title="x" * length, description="description", branch_id=1)
    with pytest.raises(InvalidLengthError):
        service.create_topic(SimpleNamespace(id=1), topic)
    service.repo.create.assert_not_called()


def test_edit_missing_topic(service):
    service.repo.get_by_id.return_value = None
    with pytest.raises(NotFoundError):
        service.edit_topic(
            SimpleNamespace(id=1, is_admin=False), 1, TopicUpdateDTO(description="new")
        )
    service.repo.update.assert_not_called()


def test_edit_topic_rejects_other_user(service):
    service.repo.get_by_id.return_value = SimpleNamespace(creator_id=2)
    with pytest.raises(PermissionDeniedError):
        service.edit_topic(
            SimpleNamespace(id=1, is_admin=False), 1, TopicUpdateDTO(description="new")
        )
    service.repo.update.assert_not_called()


def test_edit_topic_rejects_expired_edit_window(service):
    service.repo.get_by_id.return_value = SimpleNamespace(
        creator_id=1,
        created_at=datetime.now(UTC)
        - timedelta(minutes=settings.topic_edition_timeframe_minutes + 1),
    )
    with pytest.raises(PermissionDeniedError):
        service.edit_topic(
            SimpleNamespace(id=1, is_admin=False), 1, TopicUpdateDTO(description="new")
        )
    service.repo.update.assert_not_called()


def test_delete_topic_rejects_other_user(service):
    service.repo.get_by_id.return_value = SimpleNamespace(creator_id=2)
    with pytest.raises(PermissionDeniedError):
        service.delete_topic(SimpleNamespace(id=1, is_admin=False), 1)
    service.repo.update.assert_not_called()
