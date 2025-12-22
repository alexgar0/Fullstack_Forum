from datetime import datetime
from pydantic import BaseModel

class TopicCreate(BaseModel):
    title: str
    description: str | None = None
    branch_id: int

class TopicUpdate(BaseModel):
    description: str
    
class Topic(BaseModel):
    id: int
    branch_id: int
    title: str
    description: str | None = None
    creator_id: int
    is_active: bool
    created_at: datetime
    last_edited_at: datetime
    

    class Config:
        from_attributes = True