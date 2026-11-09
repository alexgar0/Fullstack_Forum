import pytest

from forum.features.user.service import password_complexity_check


@pytest.mark.parametrize(
    ("password", "valid", "message"),
    (
        ("Abc123", False, "Password must be at least 8 characters long"),
        ("abcdefg1", False, "Password must contain at least one uppercase letter"),
        ("ABCDEFG1", False, "Password must contain at least one lowercase letter"),
        ("Abcdefgh", False, "Password must contain at least one digit"),
        ("Abcdefg1", True, "Password is valid"),
    ),
)
def test_password_complexity(password, valid, message):
    assert password_complexity_check(password) == (valid, message)
