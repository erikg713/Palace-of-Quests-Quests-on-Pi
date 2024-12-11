import time
from app.models import db, Player

def test_query_performance(init_database):
    start_time = time.time()
    player = Player.query.filter_by(username="test_user").first()
    end_time = time.time()

    assert player is not None
    assert (end_time - start_time) < 0.1  # Ensure query completes within 100ms
