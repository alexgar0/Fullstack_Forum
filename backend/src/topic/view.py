
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..user.database.models import User
from ..user.session import get_current_user, get_current_user_for_activity

from .database.service import TopicService
from .schemas import Topic, TopicUpdate, TopicCreate


router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("/{topic_id}", response_model=Topic)
def read_topic(topic_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    topic_service = TopicService(db)
    topic = topic_service.get_topic(topic_id)
    return topic

@router.post("/", response_model=Topic, status_code=201)
def create_topic(topic: TopicCreate, current_user: User = Depends(get_current_user_for_activity), db: Session = Depends(get_db)):
    topic_service = TopicService(db)
    new_topic = topic_service.create_topic(current_user, topic)
    return new_topic

@router.put("/{topic_id}", response_model=Topic)
def update_topic(topic_id: int, payload: TopicUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    topic_service = TopicService(db)
    edited_topic = topic_service.edit_topic(current_user, topic_id, payload)
    return edited_topic