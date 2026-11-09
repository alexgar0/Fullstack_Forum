import pytest

from forum.features.branch.repo import BranchRepo
from forum.features.branch.schemas import BranchCreateDTO
from forum.features.branch.service import BranchService
from forum.features.topic.repo import TopicRepo
from forum.features.topic.schemas import TopicCreateDTO
from forum.features.topic.service import TopicService


@pytest.fixture
def branch_repo(db_session):
    return BranchRepo(db_session)


@pytest.fixture
def branch_service(db_session):
    return BranchService(db_session)


@pytest.fixture
def mock_branch_create_dto():
    return BranchCreateDTO(
        title="mock_branch title", description="mock_branch description"
    )


@pytest.fixture
def mock_branch(branch_service, test_user_admin, mock_branch_create_dto):
    return branch_service.create_branch(
        user=test_user_admin, branch=mock_branch_create_dto
    )


@pytest.fixture
def topic_repo(db_session):
    return TopicRepo(db_session)


@pytest.fixture
def topic_service(db_session):
    return TopicService(db_session)


@pytest.fixture
def mock_topic_create_dto(mock_branch):
    return TopicCreateDTO(
        title="mock_topic title",
        description="mock_topic description",
        branch_id=mock_branch.id,
    )


@pytest.fixture
def mock_topic(topic_service, test_user_admin, mock_topic_create_dto):
    return topic_service.create_topic(user=test_user_admin, topic=mock_topic_create_dto)
