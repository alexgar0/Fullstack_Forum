from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship


if TYPE_CHECKING:
    from forum.features.user.database.models import User


class IdMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)

class OwnableByUserMixin:
    creator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )

    @declared_attr
    def creator(cls: Any) -> Mapped[User]:
        return relationship("User", back_populates=f"created_{cls.__tablename__}")

class CreatedAtTimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )