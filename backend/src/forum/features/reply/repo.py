from sqlalchemy.orm import Session

from forum.features.common.repo import OwnableRepo, ViewableRepo
from forum.features.reply.models import Reply


class ReplyRepo(ViewableRepo[Reply], OwnableRepo[Reply]):
    def __init__(self, db: Session):
        super().__init__(db, Reply)
