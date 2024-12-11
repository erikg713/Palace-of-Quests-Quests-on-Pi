from app.models import db, Player

def test_player_query():
    player = Player.query.filter_by(username="test_user").first()
    assert player is not None
    assert player.level == 1
