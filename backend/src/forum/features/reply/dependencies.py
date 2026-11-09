from collections.abc import Generator
from typing import Annotated

from fastapi import Depends

from forum.features.common.dependencies import DatabaseDep
from forum.features.reply.service import ReplyService


def get_reply_service(
    db: DatabaseDep,
) -> Generator[ReplyService]:
    try:
        reply_service = ReplyService(db)
        yield reply_service
    finally:
        pass


ReplyServiceDep = Annotated[ReplyService, Depends(get_reply_service)]
