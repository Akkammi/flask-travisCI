import pytest
import os
from app import create_app
from app.db import User, db, Expense
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="module")
def test_client():
    os.environ["CONFIG_TYPE"] = "app.config.TestingConfig"
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        with flask_app.app_context():
            yield test_client


@pytest.fixture(scope="module")
def new_user():
    return User(username="john_doe", password="strong_password")


@pytest.fixture(scope="module")
def init_database(test_client):
    db.create_all()

    default_user = User(
        username="mary",
        password=generate_password_hash(
            password="strong_password",
            method="pbkdf2",
        ),
    )
    second_user = User(
        username="patrick",
        password=generate_password_hash(
            password="strong_password",
            method="pbkdf2",
        ),
    )
    db.session.add(default_user)
    db.session.add(second_user)
    db.session.commit()

    expense1 = Expense(title="Expense1", amount=5, user_id=default_user.id)
    expense2 = Expense(title="Expense2", amount=10, user_id=default_user.id)
    expense3 = Expense(title="Expense3", amount=15, user_id=default_user.id)
    db.session.add_all([expense1, expense2, expense3])
    db.session.commit()

    yield  # відбуваеться тетсування

    db.drop_all()


@pytest.fixture(scope="module")
def default_user_token(test_client):
    response = test_client.post(
        "/users/login",
        json={
            "username": "mary",
            "password": "strong_password",
        },
    )

    yield response.json["access_token"]


@pytest.fixture(scope="module")
def second_user_token(test_client):
    response = test_client.post(
        "/users/login",
        json={
            "username": "patrick",
            "password": "strong_password",
        },
    )

    yield response.json["access_token"]
