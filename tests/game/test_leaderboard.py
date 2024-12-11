from app.game.leaderboard import Leaderboard

def test_add_player_to_leaderboard():
    leaderboard = Leaderboard()
    leaderboard.add_player("Player1", score=150)
    leaderboard.add_player("Player2", score=200)

    top_player = leaderboard.get_top_player()
    assert top_player["username"] == "Player2"
    assert top_player["score"] == 200

def test_leaderboard_ranking():
    leaderboard = Leaderboard()
    leaderboard.add_player("Player1", score=100)
    leaderboard.add_player("Player2", score=200)
    leaderboard.add_player("Player3", score=150)

    rankings = leaderboard.get_rankings()
    assert rankings[0]["username"] == "Player2"
    assert rankings[1]["username"] == "Player3"
    assert rankings[2]["username"] == "Player1"
