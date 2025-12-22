from datetime import datetime
from typing import Optional
from pydantic import BaseModel


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

    children_ids: list[int] = []
    topic_ids: list[int] = []

    class Config:
        from_attributes = True