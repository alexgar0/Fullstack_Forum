from typing import List, Optional

from forum.features.common.repo import CRUDRepo, ViewableRepo
from forum.features.reply.database.models import Reply
from sqlalchemy.orm import Session

class ReplyRepo(CRUDRepo[Reply], ViewableRepo[Reply]):
    def __init__(self, db: Session):
        super().__init__(db, Reply)
        
    def get_replies_by_creator(self, creator_id: int) -> List[Reply]:
        return self.db.query(Reply).filter(Reply.creator_id == creator_id).all()
    