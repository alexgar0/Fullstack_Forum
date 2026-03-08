from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Enum as SqlEnum,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from forum.database import Base


class Role(str, Enum):
    admin = "admin"
    premium = "premium"
    user = "user"
    guest = "guest"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(Role), default=Role.user, nullable=False)
    bio = Column(Text)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_login = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_activity = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    created_topics = relationship(
        "Topic", back_populates="creator", cascade="all, delete-orphan", lazy="dynamic"
    )
    created_branches = relationship(
        "Branch", back_populates="creator", cascade="all, delete-orphan", lazy="dynamic"
    )
    created_replies = relationship(
        "Reply", back_populates="creator", cascade="all, delete-orphan", lazy="dynamic"
    )

    @property
    def is_admin(self):
        return self.role == Role.admin

    @property
    def is_premium(self):
        return self.role == Role.premium

    @property
    def created_topics_ids(self):
        return [topic.id for topic in self.created_topics]

    @property
    def created_branches_ids(self):
        return [branch.id for branch in self.created_branches]
