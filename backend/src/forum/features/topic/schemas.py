from datetime import datetime
from forum.features.common.schemas import BaseEntityDTO, CreatedAtDTO, OwnableDTO, ViewsDTO
from forum.features.topic.database.models import Topic
from pydantic import AliasPath, BaseModel, Field


class TopicCreateDTO(BaseModel):
    title: str
    description: str | None = None
    branch_id: int


class TopicUpdateDTO(BaseModel):
    description: str


class SmallTopicDTO(BaseEntityDTO, ViewsDTO, OwnableDTO, CreatedAtDTO):
    branch_id: int
    title: str
    last_edited_at: datetime

    class Config:
        from_attributes = True


class FullTopicDTO(SmallTopicDTO):
    is_active: bool
    description: str | None = None
    