from app.game.events import TriggerSystem

def test_level_up_event_trigger():
    triggers = TriggerSystem()
    reward = triggers.on_event("level_up", {"level": 50})
    assert reward == "Golden Crown"

def test_event_sequence():
    triggers = TriggerSystem()
    triggers.on_event("quest_completed", {"quest_id": 1})
    reward = triggers.on_event("special_event_triggered", {"event_type": "guilded_chamber"})
    assert reward == "Special Reward: Crown of Champions"
