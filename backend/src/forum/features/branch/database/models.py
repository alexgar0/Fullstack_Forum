from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship, backref
from ....database import Base
from ...topic.database.models import Topic
class Branch(Base):
    __tablename__ = "branches"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    creator_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    parent_id = Column(Integer, ForeignKey("branches.id"), index=True, nullable=True)
    
    creator = relationship("User", back_populates="created_branches")
    topics = relationship("Topic", back_populates="branch", cascade="all, delete-orphan", lazy="dynamic")
    parent = relationship("Branch", remote_side=[id], backref=backref("children", lazy="dynamic"))

    @property
    def topic_ids(self):
        return [obj[0] for obj in self.topics.with_entities(Topic.id)]
    
    @property
    def topic_titles(self):
        return[obj[0] for obj in self.topics.with_entities(Topic.title)]

    @property
    def children_ids(self):
        return [obj[0] for obj in self.children.with_entities(self.__class__.id)]
    
    @property
    def topic_count(self) -> int:
        return self.topics.count()