from datetime import timedelta, datetime, timezone
from typing import Generator, List
from fastapi import Depends
from sqlalchemy.orm import Session

from ....config import TOPIC_TITLE_LENGTH_BOUNDS, TOPIC_EDITION_TIMEFRAME_MINUTES
from ....database import get_db
from ....exceptions import InvalidLengthError, NotFoundError, PermissionDeniedError

from ...query import PaginationQuery
from ...user.database.models import User
from ..schemas import SmallTopicDTO, TopicCreateDTO, TopicUpdateDTO

from .repo import TopicRepo
from .models import Topic


class TopicService:
    def __init__(self, db: Session):
        self.repo = TopicRepo(db)

    def get_topic(self, topic_id: int) -> Topic | None:
        return self.repo.get_topic(topic_id)

    def get_small_topics_from_branch_with_pagination(self, branch_id: int, pagination: PaginationQuery) -> List[SmallTopicDTO]:
        active_topics = [topic for topic in self.repo.get_topics_by_branch(
            branch_id, pagination) if topic.is_active]
        return active_topics

    def create_topic(self, user: User, topic: TopicCreateDTO) -> Topic:
        if not (TOPIC_TITLE_LENGTH_BOUNDS[0] <= len(topic.title) <= TOPIC_TITLE_LENGTH_BOUNDS[1]):
            raise InvalidLengthError(
                min_length=TOPIC_TITLE_LENGTH_BOUNDS[0],
                max_length=TOPIC_TITLE_LENGTH_BOUNDS[1],
                message=f"Title must be between {TOPIC_TITLE_LENGTH_BOUNDS[0]} and {TOPIC_TITLE_LENGTH_BOUNDS[1]} characters long")

        new_topic = Topic(
            title=topic.title,
            description=topic.description,
            branch_id=topic.branch_id,
            creator_id=user.id
        )
        return self.repo.create_topic(new_topic)

    def edit_topic(self, user: User, topic_id: int, payload: TopicUpdateDTO) -> Topic:
        topic = self.repo.get_topic(topic_id)

        if topic.creator_id != user.id and not user.is_admin:
            raise PermissionDeniedError(
                "Only the creator or admin can edit the topic")

        if datetime.now(timezone.utc) - topic.created_at > timedelta(minutes=TOPIC_EDITION_TIMEFRAME_MINUTES) and not user.is_admin:
            raise PermissionDeniedError("Topic can no longer be edited")

        topic.description = payload.description
        return self.repo.update_topic(topic)

    def delete_topic(self, user: User, topic_id: int) -> None:
        topic = self.repo.get_topic(topic_id)

        if topic.creator_id != user.id and not user.is_admin:
            raise PermissionDeniedError(
                "Only the creator or admin can delete the topic")

        topic.is_active = False
        self.repo.update_topic(topic)


def get_topic_service(db: Session = Depends(get_db)) -> Generator[TopicService, None, None]:
    try:
        topic_service = TopicService(db)
        yield topic_service
    finally:
        pass
