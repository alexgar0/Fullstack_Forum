from pydantic import BaseModel, ConfigDict, Field

from forum.features.common.schemas import (
    BaseEntityDTO,
    CreatedAtDTO,
    OwnableDTO,
    PaginationDTO,
    ViewsDTO,
)
from forum.features.topic.schemas import SmallTopicDTO


class BranchCreateDTO(BaseModel):
    title: str
    description: str | None = None
    parent_id: int | None = None


class BranchDTO(BaseEntityDTO, ViewsDTO, OwnableDTO, CreatedAtDTO):
    title: str
    description: str | None = None
    is_active: bool
    parent_id: int | None = None
    topic_count: int
    children_ids: list[int] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class BranchWithSmallTopicsDTO(BranchDTO):
    small_topics: list[SmallTopicDTO]
    pagination: PaginationDTO
