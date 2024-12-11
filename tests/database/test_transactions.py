from app.models import db, Player

def test_transaction_commit():
    player = Player(username="test_user", level=1)
    db.session.add(player)
    db.session.commit()
    assert Player.query.count() == 1

def test_transaction_rollback():
    player = Player(username="test_user", level=1)
    db.session.add(player)
    db.session.rollback()
    assert Player.query.count() == 0
