from app.services import PlayerService

def test_level_up_player():
    service = PlayerService()
    player = service.create_player(username="test_user", level=1)
    service.level_up(player)
    assert player.level == 2

def test_get_player_rewards():
    service = PlayerService()
    player = service.create_player(username="test_user", level=10)
    rewards = service.get_rewards(player)
    assert "Golden Sword" in rewards
