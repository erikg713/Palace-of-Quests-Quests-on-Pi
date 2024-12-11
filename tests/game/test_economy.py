from app.game.economy import Economy

def test_player_balance_operations():
    economy = Economy()
    economy.add_balance(player_id=1, amount=100)
    assert economy.get_balance(player_id=1) == 100

    economy.subtract_balance(player_id=1, amount=50)
    assert economy.get_balance(player_id=1) == 50

    try:
        economy.subtract_balance(player_id=1, amount=100)
        assert False, "Should not allow overdraft"
    except ValueError:
        pass
