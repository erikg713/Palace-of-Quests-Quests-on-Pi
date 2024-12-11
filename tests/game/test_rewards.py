from app.game.rewards import distribute_rewards

def test_distribute_rewards():
    rewards = distribute_rewards(level=50)
    assert "Golden Sword" in rewards
    assert len(rewards) == 1  # Only 1 reward should be given

from app.game.rewards import calculate_rewards

def test_reward_calculation():
    rewards = calculate_rewards(level=50)
    assert "Golden Sword" in rewards
    assert "Silver Shield" not in rewards
