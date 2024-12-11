from app.game.levels import Level

def test_level_progression():
    level = Level(current=10)
    level.upgrade()
    assert level.current == 11

def test_max_level():
    level = Level(current=249)
    level.upgrade()
    assert level.current == 250
    assert not level.upgrade()  # Should not allow further upgrades
