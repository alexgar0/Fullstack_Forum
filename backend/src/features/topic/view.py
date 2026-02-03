
from typing import Generator
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...database import get_db
from ..user.database.models import User
from ..user.session import get_current_user, get_current_user_for_activity

from .database.service import TopicService
from .schemas import TopicDTO, TopicUpdateDTO, TopicCreateDTO


def get_topic_service(db: Session = Depends(get_db)) -> Generator[TopicService, None, None]:
    try:
        topic_service = TopicService(db)
        yield topic_service
    finally:
        pass


router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("/{topic_id}", response_model=TopicDTO)
def read_topic(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    topic_service: TopicService = Depends(get_topic_service)
):
    topic = topic_service.get_topic(topic_id)
    return topic


@router.post("/", response_model=TopicDTO, status_code=201)
def create_topic(
    topic: TopicCreateDTO,
    current_user: User = Depends(get_current_user_for_activity),
    topic_service: TopicService = Depends(get_topic_service)
):
    new_topic = topic_service.create_topic(current_user, topic)
    return new_topic


@router.put("/{topic_id}", response_model=TopicDTO)
def update_topic(
    topic_id: int,
    payload: TopicUpdateDTO,
    current_user: User = Depends(get_current_user),
    topic_service: TopicService = Depends(get_topic_service)
):
    edited_topic = topic_service.edit_topic(current_user, topic_id, payload)
    return edited_topic
