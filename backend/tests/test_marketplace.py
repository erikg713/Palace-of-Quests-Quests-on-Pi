import pytest
from app import create_app, db
from app.models import MarketplaceItem, User

@pytest.fixture
def app():
    """Set up Flask application for testing."""
    app = create_app('testing')  # Use a testing config
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Set up Flask test client."""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Helper fixture to create a user and generate a JWT token."""
    user_data = {'username': 'testuser', 'password': 'password123'}
    client.post('/auth/register', json=user_data)
    response = client.post('/auth/login', json=user_data)
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_get_items_empty(client):
    """Test fetching items when the database is empty."""
    response = client.get('/marketplace/items')
    assert response.status_code == 200
    assert response.json == []

def test_add_item(client, auth_headers):
    """Test adding a new marketplace item."""
    item_data = {
        'name': 'Test Item',
        'description': 'This is a test item.',
        'price': 100.0
    }
    response = client.post('/marketplace/items', json=item_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json['message'] == 'Item added successfully'

def test_add_item_missing_fields(client, auth_headers):
    """Test adding an item with missing fields."""
    item_data = {
        'name': 'Test Item',
        'price': 100.0
    }
    response = client.post('/marketplace/items', json=item_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'description' in response.json['errors']

def test_update_item(client, auth_headers):
    """Test updating an existing item."""
    # Create an item
    item = MarketplaceItem(name='Old Item', description='Old description', price=50.0, seller_id=1)
    db.session.add(item)
    db.session.commit()

    update_data = {'name': 'Updated Item', 'price': 75.0}
    response = client.put(f'/marketplace/items/{item.id}', json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json['message'] == 'Item updated successfully'

def test_update_item_not_found(client, auth_headers):
    """Test updating a non-existent item."""
    update_data = {'name': 'Non-existent Item', 'price': 75.0}
    response = client.put('/marketplace/items/999', json=update_data, headers=auth_headers)
    assert response.status_code == 404
    assert response.json['error'] == 'Item not found'

def test_delete_item(client, auth_headers):
    """Test deleting an existing item."""
    # Create an item
    item = MarketplaceItem(name='Item to delete', description='To be deleted', price=10.0, seller_id=1)
    db.session.add(item)
    db.session.commit()

    response = client.delete(f'/marketplace/items/{item.id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['message'] == 'Item deleted successfully'

def test_delete_item_not_found(client, auth_headers):
    """Test deleting a non-existent item."""
    response = client.delete('/marketplace/items/999', headers=auth_headers)
    assert response.status_code == 404
    assert response.json['error'] == 'Item not found'
def test_invalid_name(client, auth_headers):
    """Test adding an item with an invalid name."""
    item_data = {
        'name': 'a',
        'description': 'This is valid.',
        'price': 100.0
    }
    response = client.post('/marketplace/items', json=item_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'Name must be at least 3 characters long' in response.json['errors']['name']

def test_invalid_description(client, auth_headers):
    """Test adding an item with an overly long description."""
    item_data = {
        'name': 'Valid Name',
        'description': 'x' * 201,  # 201 characters
        'price': 100.0
    }
    response = client.post('/marketplace/items', json=item_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'Description must be 200 characters or less' in response.json['errors']['description']

def test_invalid_price(client, auth_headers):
    """Test adding an item with a price of zero."""
    item_data = {
        'name': 'Valid Name',
        'description': 'Valid description.',
        'price': 0
    }
    response = client.post('/marketplace/items', json=item_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'Price must be greater than zero' in response.json['errors']['price']
def test_large_price_value(client, auth_headers):
    """Test adding an item with a very large price."""
    item_data = {
        'name': 'Expensive Item',
        'description': 'This item is extremely expensive.',
        'price': 1e9  # 1 billion
    }
    response = client.post('/marketplace/items', json=item_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'Price must be between 0 and 10,000' in response.json['errors']['price']
    def test_empty_fields(client, auth_headers):
    """Test adding an item with empty required fields."""
    item_data = {
        'name': '',
        'description': '',
        'price': ''
    }
    response = client.post('/marketplace/items', json=item_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'Name is required' in response.json['errors']['name']
    assert 'Description is required' in response.json['errors']['description']
    assert 'Price is required' in response.json['errors']['price']
    def test_unauthorized_update(client, auth_headers):
    """Test updating an item that belongs to another user."""
    # Create an item for another user
    other_item = MarketplaceItem(name='Other User Item', description='Not yours.', price=20.0, seller_id=2)
    db.session.add(other_item)
    db.session.commit()

    update_data = {'name': 'Updated Name'}
    response = client.put(f'/marketplace/items/{other_item.id}', json=update_data, headers=auth_headers)
    assert response.status_code == 403
    assert response.json['error'] == 'Unauthorized action'

def test_unauthorized_delete(client, auth_headers):
    """Test deleting an item that belongs to another user."""
    # Create an item for another user
    other_item = MarketplaceItem(name='Other User Item', description='Not yours.', price=20.0, seller_id=2)
    db.session.add(other_item)
    db.session.commit()

    response = client.delete(f'/marketplace/items/{other_item.id}', headers=auth_headers)
    assert response.status_code == 403
    assert response.json['error'] == 'Unauthorized action'
    @pytest.fixture(autouse=True)
def setup_and_teardown():
    """Clear database before each test."""
    db.session.query(MarketplaceItem).delete()
    db.session.commit()
    yield
    db.session.query(MarketplaceItem).delete()
    db.session.commit()
    
