from collections.abc import Generator
from typing import Annotated

from fastapi import Depends

from forum.features.common.dependencies import DatabaseDep
from forum.features.topic.service import TopicService


def get_topic_service(
    db: DatabaseDep,
) -> Generator[TopicService]:
    try:
        topic_service = TopicService(db)
        yield topic_service
    finally:
        pass


TopicServiceDep = Annotated[TopicService, Depends(get_topic_service)]
