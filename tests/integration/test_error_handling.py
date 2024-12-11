def test_404_error(client):
    response = client.get('/api/nonexistent_route')
    assert response.status_code == 404
    assert response.json["message"] == "Resource not found"

def test_500_error(client, monkeypatch):
    def mock_function():
        raise Exception("Simulated server error")

    monkeypatch.setattr("app.routes.some_function", mock_function)
    response = client.get('/api/trigger-error')
    assert response.status_code == 500
    assert response.json["message"] == "An unexpected error occurred"
