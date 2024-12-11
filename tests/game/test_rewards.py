from app.game.rewards import calculate_rewards

def test_reward_calculation():
    rewards = calculate_rewards(level=50)
    assert "Golden Sword" in rewards
    assert "Silver Shield" not in rewards
