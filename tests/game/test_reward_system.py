from app.game.rewards import RewardSystem

def test_reward_tiers():
    rewards = RewardSystem()
    tier_1 = rewards.get_rewards_for_level(10)
    tier_2 = rewards.get_rewards_for_level(50)
    tier_3 = rewards.get_rewards_for_level(100)

    assert "Basic Sword" in tier_1
    assert "Golden Shield" in tier_2
    assert "Legendary Artifact" in tier_3

def test_reward_for_repeating_quest():
    rewards = RewardSystem()
    first_reward = rewards.get_reward("Retrieve the Artifact", player_level=20)
    second_reward = rewards.get_reward("Retrieve the Artifact", player_level=20)

    assert first_reward == "Artifact Shard"
    assert second_reward is None  # No reward for repeating the same quest
