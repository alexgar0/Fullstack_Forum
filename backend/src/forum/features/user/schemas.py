
from datetime import datetime
from pydantic import BaseModel

from .database.models import Role

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    
class User(BaseModel):
    id: int
    username: str
    role: Role
    bio: str | None = None
    created_at: datetime
    last_login: datetime
    last_activity: datetime

    class Config:
        from_attributes = True