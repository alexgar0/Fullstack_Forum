from datetime import datetime

from pydantic import BaseModel, ConfigDict

from forum.features.common.schemas import (
    BaseEntityDTO,
    CreatedAtDTO,
    OwnableDTO,
    PaginationDTO,
    ViewsDTO,
)
from forum.features.reply.schemas import ReplyDTO


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

    model_config = ConfigDict(from_attributes=True)


class FullTopicDTO(SmallTopicDTO):
    is_active: bool
    description: str | None = None
    replies: list[ReplyDTO]
    pagination: PaginationDTO | None = None
