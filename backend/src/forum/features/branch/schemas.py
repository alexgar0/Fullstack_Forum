from typing import List, Optional
from forum.features.common.schemas import (
    BaseEntityDTO,
    CreatedAtDTO,
    OwnableDTO,
    PaginationDTO,
    ViewsDTO,
)
from pydantic import BaseModel, ConfigDict

from forum.features.topic.schemas import SmallTopicDTO


class BranchCreateDTO(BaseModel):
    title: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class BranchDTO(BaseEntityDTO, ViewsDTO, OwnableDTO, CreatedAtDTO):
    title: str
    description: Optional[str] = None
    is_active: bool
    parent_id: Optional[int] = None
    topic_count: int
    children_ids: List[int] = []

    model_config = ConfigDict(from_attributes=True)


class BranchWithSmallTopicsDTO(BranchDTO):
    small_topics: List[SmallTopicDTO]
    pagination: PaginationDTO
