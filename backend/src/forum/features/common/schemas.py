from datetime import datetime

from pydantic import BaseModel


class BaseEntityDTO(BaseModel):
    id: int


class ViewsDTO(BaseModel):
    view_count: int


class OwnableDTO(BaseModel):
    creator_id: int
    creator_username: str


class CreatedAtDTO(BaseModel):
    created_at: datetime
    
class PaginationDTO(BaseModel):
    current_offset: int
    limit: int
    total_items: int
    
