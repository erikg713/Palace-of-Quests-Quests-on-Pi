from unittest.mock import MagicMock
from app.game.events import BackCastleSurvivorEvent

def test_back_castle_survivor_event() -> None:
    castle_event = BackCastleSurvivorEvent()
    castle_event.start_event = MagicMock(return_value=3)
    castle_event.complete_event = MagicMock(return_value="Castle Ownership")

    player: dict[str, str | int] = {"username": "Survivor", "level": 100}

    puzzles_completed = castle_event.start_event(player)
    assert puzzles_completed == 3, f"Expected 3 puzzles completed, but got {puzzles_completed}"

    final_reward = castle_event.complete_event(player)
    assert final_reward == "Castle Ownership", f"Expected 'Castle Ownership', but got '{final_reward}'"

def test_back_castle_survivor_event_invalid_player() -> None:
    castle_event = BackCastleSurvivorEvent()
    invalid_player = {"username": "", "level": -1}

    with pytest.raises(ValueError):
        castle_event.start_event(invalid_player)
