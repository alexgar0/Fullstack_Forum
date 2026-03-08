
from typing import Generator
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from forum.database import get_db
from forum.features.user.database.models import User
from forum.features.user.session import get_current_user, get_current_user_for_activity

from forum.features.topic.database.service import TopicService, get_topic_service
from forum.features.topic.schemas import FullTopicDTO, TopicUpdateDTO, TopicCreateDTO

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("/{topic_id}", response_model=FullTopicDTO)
def read_topic(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    topic_service: TopicService = Depends(get_topic_service)
):
    topic = topic_service.get_topic(topic_id)
    return topic


@router.post("/", response_model=FullTopicDTO, status_code=201)
def create_topic(
    topic: TopicCreateDTO,
    current_user: User = Depends(get_current_user_for_activity),
    topic_service: TopicService = Depends(get_topic_service)
):
    new_topic = topic_service.create_topic(current_user, topic)
    return new_topic


@router.put("/{topic_id}", response_model=FullTopicDTO)
def update_topic(
    topic_id: int,
    payload: TopicUpdateDTO,
    current_user: User = Depends(get_current_user),
    topic_service: TopicService = Depends(get_topic_service)
):
    edited_topic = topic_service.edit_topic(current_user, topic_id, payload)
    return edited_topic
