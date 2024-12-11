import time

def test_rate_limiting(client):
    for _ in range(10):  # Assuming a limit of 5 requests per minute
        response = client.get('/api/quests')
        assert response.status_code == 200

    # Exceed the limit
    response = client.get('/api/quests')
    assert response.status_code == 429
    assert response.json["message"] == "Rate limit exceeded. Try again later."
