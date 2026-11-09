from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import HTTPException, Request

from forum.core.auth import session
from forum.core.auth.security import create_access_token, create_refresh_token


def request_with_cookie(cookie=None):
    headers = [] if cookie is None else [(b"cookie", cookie.encode())]
    return Request({"type": "http", "headers": headers})


@pytest.mark.parametrize("cookie", ("access_token=abc", 'access_token="Bearer abc"'))
def test_get_token_from_cookie(cookie):
    assert session.get_token_from_cookie(request_with_cookie(cookie)) == "abc"


def test_get_token_from_cookie_requires_token():
    with pytest.raises(HTTPException) as exc:
        session.get_token_from_cookie(request_with_cookie())
    assert exc.value.status_code == 401
    assert exc.value.headers == {"WWW-Authenticate": "Bearer"}


@pytest.fixture
def user_service(monkeypatch):
    service = Mock()
    monkeypatch.setattr(session, "UserService", Mock(return_value=service))
    return service


@pytest.mark.parametrize(
    ("get_user", "create_token"),
    (
        (session.get_current_user, create_access_token),
        (session.get_current_user_from_refresh_token, create_refresh_token),
    ),
)
def test_valid_token_returns_user(user_service, get_user, create_token):
    user = SimpleNamespace(id=1)
    user_service.repo.get_user_by_username.return_value = user
    assert get_user(Mock(), create_token({"sub": "alice"})) is user
    user_service.repo.get_user_by_username.assert_called_once_with(username="alice")


@pytest.mark.parametrize(
    ("get_user", "create_token"),
    (
        (session.get_current_user, create_refresh_token),
        (session.get_current_user_from_refresh_token, create_access_token),
    ),
)
def test_wrong_token_type_is_rejected(user_service, get_user, create_token):
    with pytest.raises(HTTPException) as exc:
        get_user(Mock(), create_token({"sub": "alice"}))
    assert exc.value.status_code == 401
    user_service.repo.get_user_by_username.assert_not_called()


@pytest.mark.parametrize(
    ("get_user", "create_token"),
    (
        (session.get_current_user, create_access_token),
        (session.get_current_user_from_refresh_token, create_refresh_token),
    ),
)
def test_token_without_subject_is_rejected(user_service, get_user, create_token):
    with pytest.raises(HTTPException) as exc:
        get_user(Mock(), create_token({}))
    assert exc.value.status_code == 401
    user_service.repo.get_user_by_username.assert_not_called()


@pytest.mark.parametrize(
    ("get_user", "create_token"),
    (
        (session.get_current_user, create_access_token),
        (session.get_current_user_from_refresh_token, create_refresh_token),
    ),
)
def test_token_for_deleted_user_is_rejected(user_service, get_user, create_token):
    user_service.repo.get_user_by_username.return_value = None
    with pytest.raises(HTTPException) as exc:
        get_user(Mock(), create_token({"sub": "alice"}))
    assert exc.value.status_code == 401


def test_expired_access_token_is_rejected(user_service):
    token = create_access_token({"sub": "alice"}, timedelta(seconds=-1))
    with pytest.raises(HTTPException) as exc:
        session.get_current_user(Mock(), token)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Token has expired"
    user_service.repo.get_user_by_username.assert_not_called()


def test_activity_updates_authenticated_user(user_service):
    user = SimpleNamespace(id=42)
    user_service.repo.get_user_by_username.return_value = user
    result = session.get_current_user_for_activity(
        Mock(), create_access_token({"sub": "alice"})
    )
    assert result is user
    user_service.update_last_activity.assert_called_once_with(42)
