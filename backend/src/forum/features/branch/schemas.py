from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from forum.features.topic.schemas import SmallTopicDTO

class BranchCreateDTO(BaseModel):
    title: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class BranchDTO(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    creator_id: int
    is_active: bool
    created_at: datetime
    parent_id: Optional[int] = None
    topic_count: int
    children_ids: List[int] = []

    class Config:
        from_attributes = True
        
class BranchWithSmallTopicsDTO(BranchDTO):
    small_topics: List[SmallTopicDTO]