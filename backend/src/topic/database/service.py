from datetime import timedelta, datetime, timezone
from sqlalchemy.orm import Session

from ...exceptions import NotFoundError, PermissionDeniedError

from ...user.database.models import User
from ..schemas import TopicCreateDTO, TopicUpdateDTO

from .repo import TopicRepo
from .models import Topic

TITLE_MIN_LENGTH = 5
TITLE_MAX_LENGTH = 200

TOPIC_EDITION_TIMEFRAME_MINUTES = 30

class TopicService:
    def __init__(self, db: Session):
        self.repo = TopicRepo(db)

    def get_topic(self, topic_id: int) -> Topic | None:
        return self.repo.get_topic(topic_id)
    
    def create_topic(self, user: User, topic: TopicCreateDTO) -> Topic:
        if not (TITLE_MIN_LENGTH <= len(topic.title) <= TITLE_MAX_LENGTH):
            raise ValueError(
                f"Title must be between {TITLE_MIN_LENGTH} and {TITLE_MAX_LENGTH} characters long")

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
            raise PermissionDeniedError("Only the creator or admin can edit the topic")
        
        if datetime.now(timezone.utc) - topic.created_at > timedelta(minutes=TOPIC_EDITION_TIMEFRAME_MINUTES) and not user.is_admin:
            raise PermissionDeniedError("Topic can no longer be edited")

        topic.description = payload.description
        return self.repo.update_topic(topic)
    
    def delete_topic(self, user: User, topic_id: int) -> None:
        topic = self.repo.get_topic(topic_id)
        
        if topic.creator_id != user.id and not user.is_admin:
            raise PermissionDeniedError("Only the creator or admin can delete the topic")
        
        topic.is_active = False
        self.repo.update_topic(topic)