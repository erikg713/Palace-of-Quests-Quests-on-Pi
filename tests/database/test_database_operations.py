from app.models import db, Player, Quest

def test_player_and_quest_relationship(init_database):
    player = Player.query.filter_by(username="test_user").first()
    quest = Quest.query.filter_by(title="Find the Hidden Key").first()

    # Assign quest to player
    player.quests.append(quest)
    db.session.commit()

    assert quest in player.quests
    assert player in quest.players

def test_database_constraints(init_database):
    # Attempt to create a player without a username
    player = Player(level=1)
    db.session.add(player)

    try:
        db.session.commit()
        assert False, "Database should have raised an IntegrityError"
    except Exception as e:
        db.session.rollback()
        assert "IntegrityError" in str(e)
