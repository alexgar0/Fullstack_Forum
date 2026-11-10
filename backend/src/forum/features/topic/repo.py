from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from forum.core.exceptions import ExistingResourceError, NotFoundError
from forum.features.common.repo import OwnableRepo, ViewableRepo
from forum.features.topic.models import Topic


class TopicRepo(ViewableRepo[Topic], OwnableRepo[Topic]):
    def __init__(self, db: Session):
        super().__init__(db, Topic)

    def create(self, entity: Topic) -> Topic:
        try:
            return super().create(entity)
        except IntegrityError as exc:
            self.db.rollback()
            if "topics_title" in str(exc.orig):
                raise ExistingResourceError(
                    "Topic with the same title already exists"
                ) from exc
            if "topics_branch_id" in str(exc.orig):
                raise NotFoundError("Branch not found") from exc
            raise
