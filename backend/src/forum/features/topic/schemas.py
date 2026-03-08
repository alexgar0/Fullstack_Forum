from datetime import datetime
from pydantic import AliasPath, BaseModel, Field

class TopicCreateDTO(BaseModel):
    title: str
    description: str | None = None
    branch_id: int

class TopicUpdateDTO(BaseModel):
    description: str
    
class SmallTopicDTO(BaseModel):
    id: int
    branch_id: int
    title: str
    creator_id: int
    creator_username: str = Field(validation_alias=AliasPath("creator", "username"))
    created_at: datetime
    last_edited_at: datetime
    
    class Config:
        from_attributes = True
        
class FullTopicDTO(SmallTopicDTO):
    is_active: bool
    description: str | None = None