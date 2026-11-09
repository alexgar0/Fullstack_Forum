from __future__ import annotations

import enum
from datetime import datetime  # noqa: TC003
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum as SqlEnum,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DynamicMapped, Mapped, mapped_column, relationship

from forum.core.database import Base
from forum.features.common.entities import CreatedAtEntity, ViewableEntity

__all__ = ["Role", "User"]

if TYPE_CHECKING:
    from forum.features.branch.database.models import Branch
    from forum.features.reply.database.models import Reply
    from forum.features.topic.database.models import Topic


class Role(enum.StrEnum):
    admin = "admin"
    premium = "premium"
    user = "user"
    guest = "guest"


class User(Base, ViewableEntity, CreatedAtEntity):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Role] = mapped_column(SqlEnum(Role), default=Role.user, nullable=False)
    bio: Mapped[str | None] = mapped_column(Text)
    last_login: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_activity: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __init__(
        self,
        username: str,
        email: str,
        role: Role,
        hashed_password: str,
        bio: str | None = None,
    ) -> None:
        self.username = username
        self.email = email
        self.bio = bio
        self.role = role
        self.hashed_password = hashed_password

    created_topics: DynamicMapped[Topic] = relationship(
        "Topic", back_populates="creator", cascade="all, delete-orphan", lazy="dynamic"
    )
    created_branches: DynamicMapped[Branch] = relationship(
        "Branch", back_populates="creator", cascade="all, delete-orphan", lazy="dynamic"
    )
    created_replies: DynamicMapped[Reply] = relationship(
        "Reply", back_populates="creator", cascade="all, delete-orphan", lazy="dynamic"
    )

    @property
    def is_admin(self) -> bool:
        return self.role == Role.admin

    @property
    def is_premium(self) -> bool:
        return self.role == Role.premium
