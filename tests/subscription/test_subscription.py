from app.payments import SubscriptionManager

def test_renew_subscription():
    manager = SubscriptionManager()
    subscription = manager.activate_subscription(player_id=1, plan="premium")
    assert subscription["status"] == "active"

    renewed_subscription = manager.renew_subscription(player_id=1)
    assert renewed_subscription["status"] == "renewed"
    assert renewed_subscription["expiration_date"] > subscription["expiration_date"]

def test_cancel_subscription():
    manager = SubscriptionManager()
    manager.activate_subscription(player_id=1, plan="premium")
    canceled_subscription = manager.cancel_subscription(player_id=1)
    assert canceled_subscription["status"] == "canceled"
