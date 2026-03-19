from typing import List, Optional

from forum.features.query import PaginationQuery
from sqlalchemy.orm import Session

from forum.features.common.repo import CRUDRepo, OwnableRepo, ViewableRepo
from forum.features.reply.database.models import Reply


class ReplyRepo(CRUDRepo[Reply], ViewableRepo[Reply], OwnableRepo[Reply]):
    def __init__(self, db: Session):
        super().__init__(db, Reply)