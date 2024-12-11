from app.game.quests import QuestManager

def test_assign_quest():
    manager = QuestManager()
    quest = manager.create_quest("Find the Treasure", 10)
    player = manager.assign_quest(player_id=1, quest=quest)
    assert player.current_quest == quest
