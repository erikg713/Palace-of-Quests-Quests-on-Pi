from app.game.events import GuildedChamberEvent

def test_event_chamber_mechanics():
    event = GuildedChamberEvent()
    reward = event.conquer_chamber(player_level=50, attempts=3)
    assert reward == "Golden Crown"

    reward = event.conquer_chamber(player_level=20, attempts=3)
    assert reward == "No Reward - Level too low"
