from app.game.quests import QuestManager

def test_assign_quest_to_high_level_player():
    manager = QuestManager()
    quest = manager.create_quest(title="Conquer the Castle", level_required=10)
    player = manager.create_player(username="HighLevelPlayer", level=20)

    success = manager.assign_quest(player, quest)
    assert success is True
    assert quest in player.current_quests

def test_assign_quest_to_low_level_player():
    manager = QuestManager()
    quest = manager.create_quest(title="Conquer the Castle", level_required=10)
    player = manager.create_player(username="LowLevelPlayer", level=5)

    success = manager.assign_quest(player, quest)
    assert success is False
    assert quest not in player.current_quests

def test_complete_quest_and_receive_rewards():
    manager = QuestManager()
    quest = manager.create_quest(title="Retrieve the Artifact", level_required=5, reward="Artifact Shard")
    player = manager.create_player(username="QuestCompleter", level=10)
    manager.assign_quest(player, quest)

    completed = manager.complete_quest(player, quest)
    assert completed is True
    assert "Artifact Shard" in player.inventory
