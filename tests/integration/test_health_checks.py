def test_database_health_check(client):
    response = client.get('/api/health/db')
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_service_health_check(client):
    response = client.get('/api/health/service')
    assert response.status_code == 200
    assert response.json["status"] == "operational"
