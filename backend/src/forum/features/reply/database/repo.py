from typing import List, Optional

from forum.features.query import PaginationQuery
from sqlalchemy.orm import Session

from forum.features.common.repo import CRUDRepo, OwnableRepo, ViewableRepo
from forum.features.reply.database.models import Reply


class ReplyRepo(CRUDRepo[Reply], ViewableRepo[Reply], OwnableRepo[Reply]):
    def __init__(self, db: Session):
        super().__init__(db, Reply)
        
    def get_by_topic(self, topic_id: int, pagination: Optional[PaginationQuery] = None) -> List[Reply]:
        query = self.db.query(Reply).where(Reply.topic_id == topic_id).order_by(Reply.created_at.asc())
        if pagination:
            query = query.offset(pagination.offset).limit(pagination.limit)
        
        return query.all()