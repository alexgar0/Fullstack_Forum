from typing import Generator, List, Optional
from fastapi import Depends
from forum.database import get_db
from forum.exceptions import InvalidLengthError
from forum.features.query import PaginationQuery
from forum.features.reply.database.models import Reply
from sqlalchemy.orm import Session

from forum.config import settings
from forum.features.reply.database.repo import ReplyRepo
from forum.features.reply.schemas import ReplyCreateDTO, ReplyDTO
from forum.features.user.database.models import User


class ReplyService:
    def __init__(self, db: Session):
            self.repo = ReplyRepo(db)

    def create_reply(self, user: User, reply: ReplyCreateDTO) -> ReplyDTO:
        if not (
            settings.reply_content_length_bounds[0]
            <= len(reply.content)
            <= settings.reply_content_length_bounds[1]
        ):
            raise InvalidLengthError(
                min_length=settings.reply_content_length_bounds[0],
                max_length=settings.reply_content_length_bounds[1],
                message=f"Reply must be between {settings.reply_content_length_bounds[0]} and {settings.reply_content_length_bounds[1]} characters long",
            )
            
        new_reply = Reply(
            content=reply.content,
            topic_id=reply.topic_id,
            creator_id=user.id
        )
        created = self.repo.create(new_reply)
        return ReplyDTO.model_validate(created)
    
    def get_by_topic(self, topic_id: int, pagination: Optional[PaginationQuery] = None) -> List[ReplyDTO]:
        orm_models = self.repo.get_by_topic(topic_id, pagination=pagination)
        
        result = []
        for orm_model in orm_models:
            result.append(ReplyDTO.model_validate(orm_model))
        return result
    
    
def get_reply_service(
    db: Session = Depends(get_db),
) -> Generator[ReplyService, None, None]:
    try:
        reply_service = ReplyService(db)
        yield reply_service
    finally:
        pass
