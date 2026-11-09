from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from forum.core.config import settings
from forum.core.exceptions import InvalidLengthError
from forum.features.common.repo import PaginationResult
from forum.features.query import PaginationQuery
from forum.features.reply.schemas import ReplyCreateDTO
from forum.features.reply.service import ReplyService


@pytest.mark.parametrize(
    "length",
    (
        settings.reply_content_length_bounds[0] - 1,
        settings.reply_content_length_bounds[1] + 1,
    ),
)
def test_create_reply_rejects_invalid_content_length(length):
    service = ReplyService(Mock())
    service.repo = Mock()
    with pytest.raises(InvalidLengthError):
        service.create_reply(
            SimpleNamespace(id=1), ReplyCreateDTO(content="x" * length, topic_id=1)
        )
    service.repo.create.assert_not_called()


def test_create_reply_saves_content_and_returns_dto():
    service = ReplyService(Mock())
    service.repo = Mock()
    service.repo.create.return_value = SimpleNamespace(
        id=7,
        content="hello",
        topic_id=2,
        creator_id=1,
        creator_username="alice",
        view_count=0,
        created_at=datetime.now(UTC),
    )
    result = service.create_reply(
        SimpleNamespace(id=1), ReplyCreateDTO(content="hello", topic_id=2)
    )
    saved = service.repo.create.call_args.args[0]
    assert (saved.content, saved.topic_id, saved.creator_id) == ("hello", 2, 1)
    assert (result.id, result.creator_username) == (7, "alice")


def test_get_by_topic_converts_items_and_preserves_pagination():
    service = ReplyService(Mock())
    service.repo = Mock()
    reply = SimpleNamespace(
        id=7,
        content="hello",
        topic_id=2,
        creator_id=1,
        creator_username="alice",
        view_count=3,
        created_at=datetime.now(UTC),
    )
    service.repo.get_page.return_value = PaginationResult(
        items=[reply], total_items=9, current_offset=2, limit=1
    )
    pagination = PaginationQuery(offset=2, limit=1)
    result = service.get_by_topic(2, pagination)
    assert (result.total_items, result.current_offset, result.limit) == (9, 2, 1)
    assert len(result.items) == 1
    assert result.items[0].id == 7
    args, kwargs = service.repo.get_page.call_args
    assert args[0].right.value == 2
    assert kwargs["pagination"] is pagination
