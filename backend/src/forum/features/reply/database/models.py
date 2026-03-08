from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from ....database import Base


class Reply(Base):
    __tablename__ = "replies"
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    topic = relationship("Topic", back_populates="replies")
    creator = relationship("User", back_populates="created_replies")