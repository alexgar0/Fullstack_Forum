from forum.features.branch.database.repo import BranchRepo
from forum.features.branch.database.service import BranchService
from httpx import ASGITransport, AsyncClient
import pytest
import os
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from forum.features.user.session import get_current_user, get_current_user_for_activity
from forum.features.user.database.models import Role, User
from forum.main import app
from forum.database import Base, get_db


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(os.environ.get("DATABASE_URL"))
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def override_dependency(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_admin(db_session):
    user = User(
        role=Role.admin,
        email="test@test.com",
        username="testuser",
        hashed_password="fake_password",
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture(autouse=True)
def override_auth(test_user_admin):
    app.dependency_overrides[get_current_user] = lambda: test_user_admin
    app.dependency_overrides[get_current_user_for_activity] = lambda: test_user_admin
    yield
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_current_user_for_activity, None)


@pytest.fixture
def branch_repo(db_session):
    yield BranchRepo(db_session)
    
@pytest.fixture
def branch_service(db_session):
    yield BranchService(db_session)

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
