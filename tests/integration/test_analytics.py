from unittest.mock import patch

def test_analytics_event_tracking(client):
    with patch('app.analytics.track_event') as mock_track:
        response = client.get('/api/players/1')
        assert response.status_code == 200
        mock_track.assert_called_once_with("player_viewed", {"player_id": 1})
