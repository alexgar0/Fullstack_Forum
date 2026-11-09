from collections.abc import Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.community.postgres import PostgresContainer

from forum.core.auth.session import get_current_user, get_current_user_for_activity
from forum.core.database import Base, get_db
from forum.core.main import app
from forum.features.user.models import Role, User


@pytest.fixture(scope="session")
def postgres() -> Generator[PostgresContainer]:
    with PostgresContainer("postgres:17") as container:
        yield container


@pytest.fixture(scope="session")
def db_engine(postgres: PostgresContainer):
    engine = create_engine(postgres.get_connection_url())
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)  # noqa: N806
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def override_dependency(db_session, monkeypatch):
    monkeypatch.setitem(app.dependency_overrides, get_db, lambda: db_session)


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


@pytest.fixture
def override_auth(test_user_admin, monkeypatch):
    monkeypatch.setitem(
        app.dependency_overrides, get_current_user, lambda: test_user_admin
    )
    monkeypatch.setitem(
        app.dependency_overrides, get_current_user_for_activity, lambda: test_user_admin
    )


@pytest_asyncio.fixture
async def anonymous_client(override_dependency):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="https://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def client(anonymous_client, override_auth):
    return anonymous_client
