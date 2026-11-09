from sqlalchemy.orm import Session

from forum.features.common.repo import CRUDRepo, OwnableRepo, ViewableRepo
from forum.features.reply.models import Reply


class ReplyRepo(CRUDRepo[Reply], ViewableRepo[Reply], OwnableRepo[Reply]):
    def __init__(self, db: Session):
        super().__init__(db, Reply)
