from pydantic import BaseModel

from forum.features.common.schemas import (
    BaseEntityDTO,
    CreatedAtDTO,
    OwnableDTO,
    ViewsDTO,
)


class ReplyDTO(BaseEntityDTO, ViewsDTO, OwnableDTO, CreatedAtDTO):
    content: str
    topic_id: int

    class Config:
        from_attributes = True


class ReplyCreateDTO(BaseModel):
    content: str
    topic_id: int
