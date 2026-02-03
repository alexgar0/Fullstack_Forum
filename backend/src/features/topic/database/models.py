from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship
from ....database import Base

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), index=True, nullable=False)
    title = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    creator_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_edited_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    
    creator = relationship("User", back_populates="created_topics")
    branch = relationship("Branch", back_populates="topics")
    replies = relationship("Reply", back_populates="topic", cascade="all, delete-orphan", lazy="dynamic")