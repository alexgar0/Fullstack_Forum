from __future__ import annotations

from typing import TYPE_CHECKING

from forum.features.common.entities import (
    CreatedAtEntity,
    EditableEntity,
    ViewableEntity,
    OwnableEntity,
)
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, relationship

from forum.database import Base

__all__ = ["Reply"]

if TYPE_CHECKING:
    from forum.features.topic.database.models import Topic


class Reply(Base, ViewableEntity, OwnableEntity, EditableEntity):
    __tablename__ = "replies"

    content = Column(Text, nullable=False)

    topic_id = Column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    topic: Mapped["Topic"] = relationship("Topic", back_populates="replies")
