from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from forum.features.user.database.models import User

from forum.features.topic.database.models import Topic
from forum.features.query import PaginationQuery
from forum.exceptions import ExistingResourceError, NotFoundError


class TopicRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_topic(self, topic: Topic) -> Topic:
        try:
            self.db.add(topic)
            self.db.commit()
            self.db.refresh(topic)
            return topic
        except IntegrityError as e:
            self.db.rollback()
            if "topics_title" in str(e.orig):
                raise ExistingResourceError("Topic with the same title already exists")
            if "topics_branch_id" in str(e.orig):
                raise NotFoundError("Branch not found")
            raise

    def get_topic(self, topic_id: int) -> Optional[Topic]:
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        return topic

    def get_topics_by_creator(self, creator_id: int) -> list[Topic]:
        return self.db.query(Topic).filter(Topic.creator_id == creator_id).all()

    def get_topics_by_branch(
        self, branch_id: int, pagination: PaginationQuery | None
    ) -> list[Topic]:
        query = (
            self.db.query(Topic)
            .filter(Topic.branch_id == branch_id)
            .order_by(Topic.created_at.desc())
        )

        if pagination:
            offset_value = (pagination.page - 1) * pagination.limit
            query = query.offset(offset_value).limit(pagination.limit)

        return query.all()

    def update_topic(self, topic: Topic) -> Topic:
        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)
        return topic
