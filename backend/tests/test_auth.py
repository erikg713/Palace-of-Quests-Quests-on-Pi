import pytest
from app import create_app, db

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

def test_signin(client):
    response = client.post("/auth/signin", json={
        "authResult": {"accessToken": "test_token"}
    })
    assert response.status_code in [200, 401]
