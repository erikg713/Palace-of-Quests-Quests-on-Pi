import threading
from app.game.events import GuildedChamberEvent

def test_concurrent_event_participation():
    event = GuildedChamberEvent()

    def participate(player_id):
        return event.conquer_chamber(player_level=50, player_id=player_id, attempts=1)

    threads = []
    results = []
    for i in range(100):  # Simulate 100 players participating at once
        thread = threading.Thread(target=lambda: results.append(participate(i)))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    assert len(results) == 100
    assert all(reward == "Golden Crown" for reward in results)
