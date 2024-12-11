from unittest.mock import patch
import logging

def test_error_logging(client):
    with patch('app.logger.error') as mock_log:
        response = client.get('/api/nonexistent_route')
        assert response.status_code == 404
        mock_log.assert_called_once_with("404 Not Found: Resource not found")

def test_transaction_logging(client, init_database):
    with patch('app.logger.info') as mock_log:
        client.post('/api/players/1/quests', json={"quest_id": 1})
        mock_log.assert_called_with("Transaction successful for player_id: 1")
