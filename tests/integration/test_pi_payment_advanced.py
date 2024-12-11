from app.payments import PiPaymentGateway

def test_payment_with_insufficient_balance(monkeypatch):
    def mock_payment(*args, **kwargs):
        return {"status": "failed", "error": "Insufficient balance"}

    monkeypatch.setattr(PiPaymentGateway, "initiate_payment", mock_payment)
    response = PiPaymentGateway().initiate_payment(player_id=1, amount=1000)
    assert response["status"] == "failed"
    assert response["error"] == "Insufficient balance"

def test_payment_with_network_error(monkeypatch):
    def mock_payment(*args, **kwargs):
        raise Exception("Network error")

    monkeypatch.setattr(PiPaymentGateway, "initiate_payment", mock_payment)
    try:
        PiPaymentGateway().initiate_payment(player_id=1, amount=10)
        assert False, "Should have raised a network error"
    except Exception as e:
        assert "Network error" in str(e)
