import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test_blood_bank.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield TestClient(app)

    Base.metadata.drop_all(bind=engine)

    import models


@pytest.fixture
def admin_token(client):
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

    return response.json()["access_token"]


@pytest.fixture
def staff_token(client):
    client.post(
        "/auth/register",
        json={
            "username": "staff",
            "email": "staff@gmail.com",
            "password": "staff123",
            "role": "Staff"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "staff@gmail.com",
            "password": "staff123"
        }
    )

    return response.json()["access_token"]


@pytest.fixture
def admin_headers(admin_token):
    return {
        "Authorization": f"Bearer {admin_token}"
    }


@pytest.fixture
def staff_headers(staff_token):
    return {
        "Authorization": f"Bearer {staff_token}"
    }