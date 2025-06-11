# Test/marketplace.py

import pytest
from app import create_app, db
from models import User, Listing
from flask_jwt_extended import create_access_token

@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app("testing")
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

@pytest.fixture(scope="module")
def init_database():
    db.create_all()

    # Create a test user and listing
    user = User(username="market_user", email="market@example.com")
    user.set_password("testpass")
    db.session.add(user)
    db.session.commit()

    listing = Listing(
        title="Test Sword",
        description="Legendary sword of power",
        price=50,
        seller_id=user.id
    )
    db.session.add(listing)
    db.session.commit()

    yield db

    db.drop_all()

@pytest.fixture
def auth_headers():
    user = User.query.filter_by(email="market@example.com").first()
    token = create_access_token(identity=user.id)
    return {
        "Authorization": f"Bearer {token}"
    }


def test_create_listing(test_client, init_database, auth_headers):
    response = test_client.post("/marketplace/listing", json={
        "title": "Golden Shield",
        "description": "Protects against all attacks",
        "price": 75
    }, headers=auth_headers)

    assert response.status_code == 201
    assert b"Listing created successfully" in response.data


def test_get_all_listings(test_client, init_database):
    response = test_client.get("/marketplace/listings")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_listing_by_id(test_client, init_database):
    listing = Listing.query.first()
    response = test_client.get(f"/marketplace/listing/{listing.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == listing.title


def test_delete_listing(test_client, init_database, auth_headers):
    # First, create a listing to delete
    user = User.query.filter_by(email="market@example.com").first()
    new_listing = Listing(title="Delete Me", description="To be removed", price=30, seller_id=user.id)
    db.session.add(new_listing)
    db.session.commit()

    response = test_client.delete(f"/marketplace/listing/{new_listing.id}", headers=auth_headers)
    assert response.status_code == 200
    assert b"Listing deleted" in response.data
