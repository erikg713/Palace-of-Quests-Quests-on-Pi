from app.models import Player, Quest

def test_player_creation():
    player = Player(username="test_user", level=1)
    assert player.username == "test_user"
    assert player.level == 1

def test_quest_creation():
    quest = Quest(title="The Golden Quest", level_required=5)
    assert quest.title == "The Golden Quest"
    assert quest.level_required == 5
