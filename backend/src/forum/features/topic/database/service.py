from datetime import timedelta, datetime, timezone
from typing import Generator, List
from fastapi import Depends
from sqlalchemy.orm import Session

from forum.config import settings
from forum.database import get_db
from forum.exceptions import InvalidLengthError, NotFoundError, PermissionDeniedError

from forum.features.query import PaginationQuery
from forum.features.user.database.models import User
from forum.features.topic.schemas import (
    FullTopicDTO,
    SmallTopicDTO,
    TopicCreateDTO,
    TopicUpdateDTO,
)

from forum.features.topic.database.repo import TopicRepo
from forum.features.topic.database.models import Topic


class TopicService:
    def __init__(self, db: Session):
        self.repo = TopicRepo(db)

    def get_topic(self, topic_id: int) -> FullTopicDTO:
        topic = self.repo.get_by_id(topic_id)
        if not topic:
            raise NotFoundError("Topic not found")
        return FullTopicDTO.model_validate(topic)

    def get_small_topics_from_branch_with_pagination(
        self, branch_id: int, pagination: PaginationQuery
    ) -> List[SmallTopicDTO]:
        active_topics = [
            topic
            for topic in self.repo.get_topics_by_branch(branch_id, pagination)
            if topic.is_active
        ]

        result = []
        for orm_topic in active_topics:
            result.append(SmallTopicDTO.model_validate(orm_topic))

        return result

    def create_topic(self, user: User, topic: TopicCreateDTO) -> FullTopicDTO:
        if not (
            settings.topic_title_length_bounds[0]
            <= len(topic.title)
            <= settings.topic_title_length_bounds[1]
        ):
            raise InvalidLengthError(
                min_length=settings.topic_title_length_bounds[0],
                max_length=settings.topic_title_length_bounds[1],
                message=f"Title must be between {settings.topic_title_length_bounds[0]} and {settings.topic_title_length_bounds[1]} characters long",
            )

        new_topic = Topic(
            title=topic.title,
            description=topic.description,
            branch_id=topic.branch_id,
            creator_id=user.id,
        )
        created = self.repo.create(new_topic)
        return FullTopicDTO.model_validate(created)

    def edit_topic(
        self, user: User, topic_id: int, payload: TopicUpdateDTO
    ) -> FullTopicDTO:
        topic = self.repo.get_by_id(topic_id)

        if not topic:
            raise NotFoundError("Topic not found")

        if topic.creator_id != user.id and not user.is_admin:
            raise PermissionDeniedError("Only the creator or admin can edit the topic")

        if (
            datetime.now(timezone.utc) - topic.created_at
            > timedelta(minutes=settings.topic_edition_timeframe_minutes)
            and not user.is_admin
        ):
            raise PermissionDeniedError("Topic can no longer be edited")

        topic.description = payload.description
        updated = self.repo.update(topic_id, **payload.model_dump())
        return FullTopicDTO.model_validate(updated)

    def delete_topic(self, user: User, topic_id: int) -> None:
        topic = self.repo.get_by_id(topic_id)

        if topic is None:
            raise NotFoundError("Topic not found")

        if topic.creator_id != user.id and not user.is_admin:
            raise PermissionDeniedError(
                "Only the creator or admin can delete the topic"
            )

        self.repo.update(topic_id, is_active=False)


def get_topic_service(
    db: Session = Depends(get_db),
) -> Generator[TopicService, None, None]:
    try:
        topic_service = TopicService(db)
        yield topic_service
    finally:
        pass
