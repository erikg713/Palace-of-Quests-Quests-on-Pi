import threading
from app.models import Player

def create_players_concurrently():
    def create_player(i):
        player = Player(username=f"user_{i}", level=1)
        db.session.add(player)
        db.session.commit()

    threads = []
    for i in range(1000):  # Simulating 1000 player creations
        thread = threading.Thread(target=create_player, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def test_high_load():
    create_players_concurrently()
    assert Player.query.count() == 1000
