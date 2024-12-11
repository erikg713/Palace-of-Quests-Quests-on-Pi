from app.game.levels import calculate_scaling
from app.game.rewards import generate_rewards

def test_level_scaling():
    scaling_factor = calculate_scaling(level=10)
    assert scaling_factor == 1.2

    scaling_factor = calculate_scaling(level=50)
    assert scaling_factor == 2.5

def test_generate_rewards():
    rewards = generate_rewards(level=100)
    assert "Legendary Sword" in rewards
    assert len(rewards) == 1
