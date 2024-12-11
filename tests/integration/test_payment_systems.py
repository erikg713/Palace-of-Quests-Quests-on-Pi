from app.payments import PiPaymentGateway

def test_pi_payment_initiation():
    gateway = PiPaymentGateway()
    response = gateway.initiate_payment(player_id=1, amount=10)
    assert response["status"] == "success"
    assert response["transaction_id"] is not None

from app.payments import PiPaymentGateway

def test_pi_payment_success():
    gateway = PiPaymentGateway()
    response = gateway.initiate_payment(player_id=1, amount=10)
    assert response["status"] == "success"
    assert response["transaction_id"] is not None
