import pytest
from app.game.economy import Economy

def test_player_balance_operations():
    """
    Test basic balance operations for a player in the Economy class.
    """
    economy = Economy()

    # Test adding balance
    economy.add_balance(player_id=1, amount=100)
    assert economy.get_balance(player_id=1) == 100, "Balance should be 100 after adding 100."

    # Test subtracting balance
    economy.subtract_balance(player_id=1, amount=50)
    assert economy.get_balance(player_id=1) == 50, "Balance should be 50 after subtracting 50."

    # Test overdraft protection
    with pytest.raises(ValueError, match=".*"):
        economy.subtract_balance(player_id=1, amount=100)
