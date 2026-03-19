from __future__ import annotations

from typing import TYPE_CHECKING

from forum.features.common.entities import (
    CreatedAtEntity,
    EditableEntity,
    ViewableEntity,
    OwnableEntity,
)
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from forum.database import Base

__all__ = ["Reply"]

if TYPE_CHECKING:
    from forum.features.topic.database.models import Topic


class Reply(Base, ViewableEntity, OwnableEntity, EditableEntity):
    __tablename__ = "replies"

    content: Mapped[str] = mapped_column(Text, nullable=False)

    topic_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    topic: Mapped["Topic"] = relationship("Topic", back_populates="replies")

    
    def __init__(self, content: str, topic_id: int, creator_id: int) -> None:
        self.content = content
        self.topic_id = topic_id
        self.creator_id = creator_id