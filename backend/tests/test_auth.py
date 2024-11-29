# Unit tests
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client
    with app.app_context():
        db.drop_all()

@pytest.fixture
def mock_user(client):
    # Creating a mock user for testing purposes
    user = User(username="testuser", password="testpassword", wallet_address="mock_address")
    db.session.add(user)
    db.session.commit()
    return user

def test_signin_valid_token(client, mock_user):
    # Simulate sending a valid access token
    response = client.post("/auth/signin", json={
        "authResult": {"accessToken": "valid_token"}
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data  # Assuming the response includes a token

def test_signin_invalid_token(client):
    # Simulate sending an invalid access token
    response = client.post("/auth/signin", json={
        "authResult": {"accessToken": "invalid_token"}
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data  # Assuming the response includes an error message

def test_signin_no_token(client):
    # Simulate sending no token at all
    response = client.post("/auth/signin", json={})
    assert response.status_code == 400  # Or 401, depending on your implementation
    data = response.get_json()
    assert "error" in data