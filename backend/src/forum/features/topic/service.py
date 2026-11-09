from collections.abc import Generator
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from forum.config import settings
from forum.exceptions import InvalidLengthError, NotFoundError, PermissionDeniedError
from forum.features.common.dependencies import DatabaseDep
from forum.features.common.repo import PaginationResult
from forum.features.query import PaginationQuery
from forum.features.reply.service import ReplyService
from forum.features.topic.database.models import Topic
from forum.features.topic.database.repo import TopicRepo
from forum.features.topic.schemas import (
    FullTopicDTO,
    SmallTopicDTO,
    TopicCreateDTO,
    TopicUpdateDTO,
)
from forum.features.user.database.models import User


class TopicService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TopicRepo(db)

    def get_topic(
        self, topic_id: int, pagination: PaginationQuery | None = None
    ) -> FullTopicDTO:
        topic = self.repo.get_by_id(topic_id)
        if not topic:
            raise NotFoundError("Topic not found")
        self.repo.increment_views(topic_id)
        dto = FullTopicDTO.model_validate(topic)

        reply_service = ReplyService(self.db)
        pagination_result = reply_service.get_by_topic(topic_id, pagination=pagination)
        dto.replies = list(pagination_result.items)
        dto.pagination = pagination_result.to_dto()
        return dto

    def get_small_topics_from_branch_with_pagination(
        self, branch_id: int, pagination: PaginationQuery | None = None
    ) -> PaginationResult[SmallTopicDTO]:
        active_topics = self.repo.get_page(
            Topic.branch_id == branch_id, Topic.is_active, pagination=pagination
        )

        result = [
            SmallTopicDTO.model_validate(orm_topic)
            for orm_topic in list(active_topics.items)
        ]

        return PaginationResult(
            items=result,
            current_offset=active_topics.current_offset,
            total_items=active_topics.total_items,
            limit=active_topics.limit,
        )

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
            datetime.now(UTC) - topic.created_at
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
    db: DatabaseDep,
) -> Generator[TopicService]:
    try:
        topic_service = TopicService(db)
        yield topic_service
    finally:
        pass
