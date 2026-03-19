from __future__ import annotations

from typing import Optional

from forum.features.branch.database.models import Branch
from forum.features.common.entities import (
    CreatedAtEntity,
    ViewableEntity,
    OwnableEntity,
)
from forum.features.reply.database.models import Reply
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DynamicMapped, Mapped, mapped_column, relationship
from forum.database import Base


class Topic(Base, ViewableEntity, OwnableEntity, CreatedAtEntity):
    __tablename__ = "topics"

    branch_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("branches.id"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_edited_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    branch: Mapped[Branch] = relationship("Branch", back_populates="topics")
    replies: DynamicMapped[Reply] = relationship(
        "Reply", back_populates="topic", cascade="all, delete-orphan", lazy="dynamic"
    )

    def __init__(
        self,
        title: str,
        branch_id: int,
        creator_id: int,
        description: Optional[str] = None,
    ) -> None:
        self.title = title
        self.description = description
        self.branch_id = branch_id
        self.creator_id = creator_id
