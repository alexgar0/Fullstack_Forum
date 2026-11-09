from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from forum.core.config import settings
from forum.core.exceptions import InvalidLengthError
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
