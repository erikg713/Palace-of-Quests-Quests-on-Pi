from app.models import db, Player

def test_create_player():
    player = Player(username="test_user", level=1)
    db.session.add(player)
    db.session.commit()
    assert Player.query.filter_by(username="test_user").first() is not None
