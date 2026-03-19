
from forum.features.common.repo import CRUDRepo, OwnableRepo, ViewableRepo
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from forum.features.topic.database.models import Topic
from forum.features.query import PaginationQuery
from forum.exceptions import ExistingResourceError, NotFoundError


class TopicRepo(CRUDRepo[Topic], ViewableRepo[Topic], OwnableRepo[Topic]):
    def __init__(self, db: Session):
        super().__init__(db, Topic)

    def create(self, entity: Topic) -> Topic:
        try:
            return super().create(entity)
        except IntegrityError as e:
            self.db.rollback()
            if "topics_title" in str(e.orig):
                raise ExistingResourceError("Topic with the same title already exists")
            if "topics_branch_id" in str(e.orig):
                raise NotFoundError("Branch not found")
            raise

    def get_topics_by_branch(
        self, branch_id: int, pagination: PaginationQuery | None
    ) -> list[Topic]:
        query = (
            self.db.query(Topic)
            .filter(Topic.branch_id == branch_id)
            .order_by(Topic.created_at.desc())
        )

        if pagination:
            query = query.offset(pagination.limit).limit(pagination.limit)

        return query.all()
