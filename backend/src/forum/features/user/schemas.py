from datetime import datetime

from pydantic import BaseModel, ConfigDict

from forum.features.common.schemas import BaseEntityDTO, CreatedAtDTO, ViewsDTO
from forum.features.user.models import Role


class UserBase(BaseModel):
    username: str
    email: str


class RegisterDTO(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserDTO(BaseEntityDTO, ViewsDTO, CreatedAtDTO):
    username: str
    role: Role
    bio: str | None = None
    last_login: datetime
    last_activity: datetime

    model_config = ConfigDict(from_attributes=True)
