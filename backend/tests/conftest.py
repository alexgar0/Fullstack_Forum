from datetime import datetime, timezone
from httpx import ASGITransport, AsyncClient
import pytest
import os
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.features.user.session import get_current_user, get_current_user_for_activity
from src.features.user.database.models import User
from src.main import app
from src.database import Base, get_db


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
    now = datetime.now(timezone.utc)
    user = User(
        role="admin",
        email="test@test.com",
        username="testuser",
        hashed_password="fake_password",
        created_at=now,
        last_activity=now,
        last_login=now,
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


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
