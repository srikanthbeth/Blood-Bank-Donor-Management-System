def test_register_admin(client):

    response = client.post(
        "/auth/register",
        json={
            "username": "admin",
            "email": "admin@gmail.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "admin"
    assert data["email"] == "admin@gmail.com"
    assert data["role"] == "Admin"


def test_duplicate_email(client):

    client.post(
        "/auth/register",
        json={
            "username": "admin",
            "email": "admin@gmail.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "admin2",
            "email": "admin@gmail.com",
            "password": "123456",
            "role": "Admin"
        }
    )

    assert response.status_code == 400


def test_login(client):

    client.post(
        "/auth/register",
        json={
            "username": "admin",
            "email": "admin@gmail.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "admin@gmail.com",
            "password": "admin123"
        }
    )

    assert response.status_code == 200

    assert "access_token" in response.json()