from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .models import Topic
from ....exceptions import ExistingResourceError, NotFoundError
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
            if 'topics_title' in str(e.orig):
                raise ExistingResourceError("Topic with the same title already exists")
            if "topics_branch_id" in str(e.orig):
                raise NotFoundError("Branch not found")
            raise
                
    def get_topic(self, topic_id: int) -> Topic:
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        if topic is None:
            raise NotFoundError("Topic not found")
        return topic
    
    def get_topics_by_creator(self, creator_id: int) -> list[Topic]:
        return self.db.query(Topic).filter(Topic.creator_id == creator_id).all()
    
    def get_topics_by_branch(self, branch_id: int) -> list[Topic]:
        return self.db.query(Topic).filter(Topic.branch_id == branch_id).all()
    
    def update_topic(self, topic: Topic) -> Topic:
        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)
        return topic