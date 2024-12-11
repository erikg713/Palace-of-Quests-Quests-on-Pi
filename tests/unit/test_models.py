from app.models import Player, Quest

def test_player_creation():
    player = Player(username="test_user", level=1)
    assert player.username == "test_user"
    assert player.level == 1
