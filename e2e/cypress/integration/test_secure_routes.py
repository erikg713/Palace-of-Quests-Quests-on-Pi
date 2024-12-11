def test_protected_route_no_auth(client):
    response = client.get('/api/protected')
    assert response.status_code == 401

def test_protected_route_with_auth(client, init_database):
    login_data = {"username": "test_user", "password": "password123"}
    login_response = client.post('/api/auth/login', json=login_data)
    token = login_response.json['access_token']

    response = client.get('/api/protected', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
