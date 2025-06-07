import pytest
from app import create_app, db
from app.models import User

TEST_USERNAME = "testuser"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "password123"

@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def register_user(client, username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD):
    return client.post('/auth/register', json={
        "username": username,
        "email": email,
        "password": password
    })

def login_user(client, email=TEST_EMAIL, password=TEST_PASSWORD):
    return client.post('/auth/login', json={
        "email": email,
        "password": password
    })

def test_register_success(client, app):
    response = register_user(client)
    assert response.status_code == 201
    assert b"User registered successfully" in response.data
    with app.app_context():
        user = User.query.filter_by(email=TEST_EMAIL).first()
        assert user is not None
        assert user.username == TEST_USERNAME

@pytest.mark.parametrize("payload, status_code", [
    ({"username": "", "email": TEST_EMAIL, "password": TEST_PASSWORD}, 400),
    ({"username": TEST_USERNAME, "email": "", "password": TEST_PASSWORD}, 400),
    ({"username": TEST_USERNAME, "email": TEST_EMAIL, "password": ""}, 400),
    ({}, 400),
])
def test_register_invalid_payload(client, payload, status_code):
    response = client.post('/auth/register', json=payload)
    assert response.status_code == status_code

def test_register_duplicate_email(client):
    register_user(client)
    response = register_user(client)
    assert response.status_code == 400
    assert b"Email already registered" in response.data or b"already" in response.data

def test_login_success(client):
    register_user(client)
    response = login_user(client)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data and "access_token" in json_data

def test_login_invalid_password(client):
    register_user(client)
    response = login_user(client, password="wrongpassword")
    assert response.status_code == 401
    assert b"Invalid credentials" in response.data or b"invalid" in response.data

def test_login_nonexistent_email(client):
    response = login_user(client, email="nonexistent@example.com")
    assert response.status_code == 401
    assert b"Invalid credentials" in response.data or b"invalid" in response.data
