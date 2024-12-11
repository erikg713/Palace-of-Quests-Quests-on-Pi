from app.utils import calculate_experience_points

def test_calculate_experience_points():
    exp_points = calculate_experience_points(level=5)
    assert exp_points == 150
