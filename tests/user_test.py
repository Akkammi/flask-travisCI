def test_valid_registration(test_client, init_database):
    response = test_client.post(
        "/users/",
        json={
            "username": "test_username",
            "password": "test_password",
        },
    )

    assert response.status_code == 201
    assert "id" in response.json
    assert "username" in response.json
    assert "password" not in response.json


def test_invalid_registration(test_client, init_database):
    response = test_client.post(
        "/users/",
        json={
            "username": "test_username",
            "password": "123",
        },
    )

    assert response.status_code == 422
    assert "password" in response.json
    assert response.json["password"] == ["Shorter than minimum length 4."]


def test_dublicate_registration(test_client, init_database):
    test_client.post(
        "/users/",
        json={
            "username": "test_username",
            "password": "test_password",
        },
    )

    response = test_client.post(
        "/users/",
        json={
            "username": "test_username",
            "password": "test_password",
        },
    )

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "Користувач з таким username вже існує!"


def test_valid_login(test_client, init_database):
    response = test_client.post(
        "/users/login",
        json={
            "username": "mary",
            "password": "strong_password",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json


def test_invalid_login(test_client, init_database):
    response = test_client.post(
        "/users/login",
        json={
            "username": "mary",
            "password": "wrong_password",
        },
    )

    assert response.status_code == 401
    assert "error" in response.json
    assert response.json["error"] == "Не правильний username або password!"
