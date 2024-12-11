def test_player_creation_with_long_username(init_database):
    long_username = "a" * 256  # Exceeds max length
    player = Player(username=long_username, level=1)
    try:
        db.session.add(player)
        db.session.commit()
        assert False, "Should have raised an IntegrityError"
    except Exception as e:
        db.session.rollback()
        assert "Data too long" in str(e)

def test_quest_assignment_beyond_level(init_database):
    player = Player.query.filter_by(username="test_user").first()
    high_level_quest = Quest(title="Impossible Quest", level_required=50)
    db.session.add(high_level_quest)
    db.session.commit()

    # Attempt to assign a quest that's too difficult
    try:
        player.quests.append(high_level_quest)
        db.session.commit()
        assert False, "Should have failed due to level mismatch"
    except Exception as e:
        db.session.rollback()
        assert "level mismatch" in str(e)
