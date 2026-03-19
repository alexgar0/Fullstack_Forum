from fastapi import APIRouter, Depends

from forum.features.query import PaginationQuery
from forum.features.user.database.models import User
from forum.features.user.session import get_current_user, get_current_user_for_activity

from forum.features.topic.database.service import TopicService, get_topic_service
from forum.features.topic.schemas import FullTopicDTO, TopicUpdateDTO, TopicCreateDTO

router = APIRouter(prefix="/topics", tags=["Topics"])


@router.get("/{topic_id}", response_model=FullTopicDTO)
def read_topic(
    topic_id: int,
    pagination: PaginationQuery = Depends(PaginationQuery),
    current_user: User = Depends(get_current_user),
    topic_service: TopicService = Depends(get_topic_service),
) -> FullTopicDTO:
    topic = topic_service.get_topic(topic_id, pagination)
    return topic


@router.post("/", response_model=FullTopicDTO, status_code=201)
def create_topic(
    topic: TopicCreateDTO,
    current_user: User = Depends(get_current_user_for_activity),
    topic_service: TopicService = Depends(get_topic_service),
) -> FullTopicDTO:
    new_topic = topic_service.create_topic(current_user, topic)
    return new_topic


@router.put("/{topic_id}", response_model=FullTopicDTO)
def update_topic(
    topic_id: int,
    payload: TopicUpdateDTO,
    current_user: User = Depends(get_current_user),
    topic_service: TopicService = Depends(get_topic_service),
) -> FullTopicDTO:
    edited_topic = topic_service.edit_topic(current_user, topic_id, payload)
    return edited_topic


@router.delete("/{topic_id}", response_model=None)
def delete_topic(
    topic_id: int,
    current_user: User = Depends(get_current_user_for_activity),
    topic_service: TopicService = Depends(get_topic_service),
) -> None:
    topic_service.delete_topic(current_user, topic_id)
