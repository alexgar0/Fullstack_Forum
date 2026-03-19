from pydantic import AliasPath, BaseModel, Field

class BaseEntityDTO(BaseModel):
    id: int
    
class ViewsDTO(BaseModel):
    view_count: int
    
class OwnableDTO(BaseModel):
    creator_id: int
    creator_username: str