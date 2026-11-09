from typing import Annotated

from fastapi import Depends

from forum.features.topic.service import TopicService, get_topic_service

TopicServiceDep = Annotated[TopicService, Depends(get_topic_service)]
