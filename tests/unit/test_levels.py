from app.game.levels import Level

def test_level_progression():
    level = Level(current=10)
    level.upgrade()
    assert level.current == 11
