import pytest


@pytest.mark.asyncio
async def test_register_login_logout(client, db_session):

    # Registration
    registration_data = {
        "username": "qwerty",
        "email": "qwerty123@gmail.com",
        "password": "123Qwerty",
    }

    response = await client.post("/users/register", json=registration_data)
    assert response.status_code == 201

    data = response.json()
    assert data["username"] == registration_data["username"]

    # Login with username
    login_data = {
        "username": registration_data["username"],
        "password": registration_data["password"],
    }

    response = await client.post("/users/login", data=login_data)
    assert response.status_code == 200

    # Login with email
    login_data = {
        "username": registration_data["email"],
        "password": registration_data["password"],
    }
    response = await client.post("/users/login", data=login_data)

    assert response.status_code == 200
    assert response.json() == {"status": "success"}
    
    # Test me endpoint
    response = await client.get("/users/me")
    assert response.status_code == 200

    # Cookies
    access_token_cookie = response.cookies.get("access_token")
    refresh_token_cookie = response.cookies.get("refresh_token")
    assert access_token_cookie is not None
    assert refresh_token_cookie is not None
    assert access_token_cookie != refresh_token_cookie
    assert len(access_token_cookie) > 40
    assert len(refresh_token_cookie) > 40

    # Logout
    response = await client.post("/users/logout")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    cookies_headers = response.headers.get_list("set-cookie")

    all_headers = "; ".join(cookies_headers).lower()
    assert "access_token=" in all_headers
    assert "refresh_token=" in all_headers
    assert "max-age=0" in all_headers or "1970" in all_headers


@pytest.mark.asyncio
async def test_wrong_credentials(client, db_session):
    login_data = {
        "username": "non_existant_user",
        "password": "non_existant_user_password",
    }
    response = await client.post("/users/login", data=login_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_weak_password_registration(client, db_session):
    weak_passwords = [
        "qwerty",
        "123456",
        "Qwerty",
        "trynDdgkfng",
        "12345678qFGDFHKFDMHDFKLGDF",
    ]
    for weak_password in weak_passwords:
        registration_data = {
            "username": f"test_user{weak_password}",
            "email": f"test{weak_password}@test.com",
            "password": weak_password,
        }
        response = await client.post("/users/register", json=registration_data)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_existing_registration(client, db_session):
    existing_user = {
        "username": "qwerty",
        "email": "qwerty123@gmail.com",
        "password": "123Qwerty",
    }
    response = await client.post("/users/register", json=existing_user)
    assert response.status_code == 201

    user_with_same_email = {
        "username": existing_user["username"] + "123",
        "email": "qwerty123@gmail.com",
        "password": existing_user["password"],
    }
    response = await client.post("/users/register", json=user_with_same_email)
    assert response.status_code == 409

    user_with_same_username = {
        "username": existing_user["username"],
        "email": "qwerty123@gmail.com" + "123",
        "password": existing_user["password"],
    }
    response = await client.post("/users/register", json=user_with_same_username)
    assert response.status_code == 409
