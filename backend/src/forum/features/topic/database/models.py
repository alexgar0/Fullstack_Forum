from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DynamicMapped, Mapped, mapped_column, relationship

from forum.core.database import Base
from forum.features.common.entities import (
    EditableEntity,
    OwnableEntity,
    ViewableEntity,
)

if TYPE_CHECKING:
    from forum.features.branch.database.models import Branch
    from forum.features.reply.database.models import Reply


class Topic(Base, ViewableEntity, OwnableEntity, EditableEntity):
    __tablename__ = "topics"

    branch_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("branches.id"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    branch: Mapped[Branch] = relationship("Branch", back_populates="topics")
    replies: DynamicMapped[Reply] = relationship(
        "Reply", back_populates="topic", cascade="all, delete-orphan", lazy="dynamic"
    )

    def __init__(
        self,
        title: str,
        branch_id: int,
        creator_id: int,
        description: str | None = None,
    ) -> None:
        self.title = title
        self.description = description
        self.branch_id = branch_id
        self.creator_id = creator_id
