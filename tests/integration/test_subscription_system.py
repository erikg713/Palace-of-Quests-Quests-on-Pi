from app.payments import SubscriptionManager

def test_activate_subscription():
    manager = SubscriptionManager()
    response = manager.activate_subscription(player_id=1, plan="premium")
    assert response["status"] == "active"
    assert response["plan"] == "premium"
    assert response["expiration_date"] is not None

def test_expired_subscription_access():
    manager = SubscriptionManager()
    manager.activate_subscription(player_id=1, plan="premium")

    # Simulate expiration
    manager.expire_subscription(player_id=1)
    access = manager.check_subscription_access(player_id=1)
    assert access is False
