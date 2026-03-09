from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from forum.features.common.mixins import IdMixin
from forum.features.user.database.models import User
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DynamicMapped, Mapped, mapped_column, relationship, backref
from forum.database import Base

__all__ = ["Branch"]

if TYPE_CHECKING:
    from forum.features.topic.database.models import Topic
    from forum.features.user.database.models import User


class Branch(Base, IdMixin):
    __tablename__ = "branches"

    title: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    creator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    parent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("branches.id"), index=True, nullable=True
    )

    creator: Mapped["User"] = relationship("User", back_populates="created_branches")
    topics: DynamicMapped["Topic"] = relationship(
        "Topic", back_populates="branch", cascade="all, delete-orphan", lazy="dynamic"
    )
    parent: Mapped[Optional["Branch"]] = relationship(
        "Branch", remote_side=lambda: [Branch.__table__.c.id],
        backref=backref("children", lazy="dynamic")
    )

    if TYPE_CHECKING:
        children: DynamicMapped["Branch"]
