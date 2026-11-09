from pydantic import BaseModel, ConfigDict

from forum.features.common.schemas import (
    BaseEntityDTO,
    CreatedAtDTO,
    OwnableDTO,
    ViewsDTO,
)


class ReplyDTO(BaseEntityDTO, ViewsDTO, OwnableDTO, CreatedAtDTO):
    content: str
    topic_id: int

    model_config = ConfigDict(from_attributes=True)


class ReplyCreateDTO(BaseModel):
    content: str
    topic_id: int
