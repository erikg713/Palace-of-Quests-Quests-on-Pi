def assert_player_level(player, expected_level):
    assert player.level == expected_level, f"Expected level {expected_level}, got {player.level}"

def assert_response_status(response, expected_status):
    assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"
