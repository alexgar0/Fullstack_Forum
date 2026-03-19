from datetime import datetime
from typing import List, Optional
from forum.features.common.schemas import BaseEntityDTO, OwnableDTO, ViewsDTO
from pydantic import BaseModel, ConfigDict

from forum.features.topic.schemas import SmallTopicDTO


class BranchCreateDTO(BaseModel):
    title: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class BranchDTO(BaseEntityDTO, ViewsDTO, OwnableDTO):
    title: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    parent_id: Optional[int] = None
    topic_count: int
    children_ids: List[int] = []

    model_config = ConfigDict(from_attributes=True)


class BranchWithSmallTopicsDTO(BranchDTO):
    small_topics: List[SmallTopicDTO]
