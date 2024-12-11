from unittest.mock import MagicMock
from app.payments import PiPaymentGateway

def test_successful_payment(client, monkeypatch):
    mock_response = {"status": "success", "transaction_id": "12345"}
    monkeypatch.setattr(PiPaymentGateway, "initiate_payment", MagicMock(return_value=mock_response))

    response = client.post('/api/payments', json={"player_id": 1, "amount": 10})
    assert response.status_code == 200
    assert response.json["transaction_id"] == "12345"

def test_failed_payment(client, monkeypatch):
    mock_response = {"status": "failed", "error": "Insufficient balance"}
    monkeypatch.setattr(PiPaymentGateway, "initiate_payment", MagicMock(return_value=mock_response))

    response = client.post('/api/payments', json={"player_id": 1, "amount": 1000})
    assert response.status_code == 400
    assert response.json["error"] == "Insufficient balance"
