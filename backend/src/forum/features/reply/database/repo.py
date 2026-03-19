from typing import List, Optional

from forum.features.common.repo import CRUDRepo, OwnableRepo, ViewableRepo
from forum.features.reply.database.models import Reply
from sqlalchemy.orm import Session

class ReplyRepo(CRUDRepo[Reply], ViewableRepo[Reply], OwnableRepo[Reply]):
    def __init__(self, db: Session):
        super().__init__(db, Reply)
    