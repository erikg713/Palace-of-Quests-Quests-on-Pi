from app.game.events import BackCastleSurvivorEvent

def test_back_castle_survivor_event():
    event = BackCastleSurvivorEvent()
    player = {"username": "Survivor", "level": 100}

    puzzles_completed = event.start_event(player)
    assert puzzles_completed == 3

    final_reward = event.complete_event(player)
    assert final_reward == "Castle Ownership"
