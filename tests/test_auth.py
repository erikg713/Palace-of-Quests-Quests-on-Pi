import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register(client):
    response = client.post('/auth/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert b"User registered successfully" in response.data

def test_login(client):
    client.post('/auth/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post('/auth/login', json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.get_json()
