from unittest.mock import MagicMock
from app.cross_chain import Bridge

def test_bridge_transfer_to_ethereum(monkeypatch):
    mock_response = {"status": "success", "tx_hash": "0xabc123"}
    monkeypatch.setattr(Bridge, "transfer_to_ethereum", MagicMock(return_value=mock_response))

    response = Bridge().transfer_to_ethereum(player_id=1, amount=100)
    assert response["status"] == "success"
    assert response["tx_hash"] == "0xabc123"
