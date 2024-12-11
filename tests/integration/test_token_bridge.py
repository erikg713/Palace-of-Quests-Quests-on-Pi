from unittest.mock import MagicMock
from app.cross_chain import TokenBridge

def test_bridge_to_polygon(monkeypatch):
    mock_response = {"status": "success", "tx_hash": "0xpolygon123"}
    monkeypatch.setattr(TokenBridge, "bridge_to_polygon", MagicMock(return_value=mock_response))

    response = TokenBridge().bridge_to_polygon(player_id=1, amount=500)
    assert response["status"] == "success"
    assert response["tx_hash"] == "0xpolygon123"
