from unittest.mock import Mock

import pytest

from forum.core import database


def test_get_db_commits_and_closes(monkeypatch):
    db = Mock()
    monkeypatch.setattr(database, "SessionLocal", Mock(return_value=db))
    generator = database.get_db()
    assert next(generator) is db
    with pytest.raises(StopIteration):
        next(generator)
    db.commit.assert_called_once_with()
    db.rollback.assert_not_called()
    db.close.assert_called_once_with()


def test_get_db_rolls_back_and_closes_on_error(monkeypatch):
    db = Mock()
    monkeypatch.setattr(database, "SessionLocal", Mock(return_value=db))
    generator = database.get_db()
    assert next(generator) is db
    with pytest.raises(ValueError, match="failure"):
        generator.throw(ValueError("failure"))
    db.commit.assert_not_called()
    db.rollback.assert_called_once_with()
    db.close.assert_called_once_with()


def test_get_db_rolls_back_when_commit_fails(monkeypatch):
    db = Mock()
    db.commit.side_effect = ValueError("commit failed")
    monkeypatch.setattr(database, "SessionLocal", Mock(return_value=db))
    generator = database.get_db()
    assert next(generator) is db
    with pytest.raises(ValueError, match="commit failed"):
        next(generator)
    db.rollback.assert_called_once_with()
    db.close.assert_called_once_with()
