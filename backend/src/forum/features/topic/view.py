from typing import Annotated

from fastapi import APIRouter, Depends

from forum.features.query import PaginationQuery
from forum.features.topic.dependencies import TopicServiceDep
from forum.features.topic.schemas import FullTopicDTO, TopicCreateDTO, TopicUpdateDTO
from forum.features.user.database.models import User
from forum.features.user.session import get_current_user, get_current_user_for_activity

router = APIRouter(prefix="/topics", tags=["Topics"])


@router.get(
    "/{topic_id}", response_model=FullTopicDTO, dependencies=[Depends(get_current_user)]
)
def read_topic(
    topic_id: int,
    pagination: Annotated[PaginationQuery, Depends(PaginationQuery)],
    topic_service: TopicServiceDep,
) -> FullTopicDTO:
    return topic_service.get_topic(topic_id, pagination)


@router.post("/", response_model=FullTopicDTO, status_code=201)
def create_topic(
    topic: TopicCreateDTO,
    current_user: Annotated[User, Depends(get_current_user_for_activity)],
    topic_service: TopicServiceDep,
) -> FullTopicDTO:
    return topic_service.create_topic(current_user, topic)


@router.put("/{topic_id}", response_model=FullTopicDTO)
def update_topic(
    topic_id: int,
    payload: TopicUpdateDTO,
    current_user: Annotated[User, Depends(get_current_user)],
    topic_service: TopicServiceDep,
) -> FullTopicDTO:
    return topic_service.edit_topic(current_user, topic_id, payload)


@router.delete("/{topic_id}", response_model=None)
def delete_topic(
    topic_id: int,
    topic_service: TopicServiceDep,
    current_user: Annotated[User, Depends(get_current_user_for_activity)],
) -> None:
    topic_service.delete_topic(current_user, topic_id)
