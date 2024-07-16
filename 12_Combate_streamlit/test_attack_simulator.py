import random
from unittest.mock import patch

# Import the function we want to test
from main import simulate_attack_roll

def test_simulate_attack_roll():
    # Set a fixed seed for reproducibility
    random.seed(42)

    # Test case 1: Basic functionality
    result = simulate_attack_roll(5, "1d8")
    print("Test case 1 result:", result)
    assert isinstance(result, dict), "Result should be a dictionary"
    assert all(key in result for key in ['d20_roll', 'total_attack', 'damage_roll', 'total_damage']), "Result should contain all expected keys"
    assert 1 <= result['d20_roll'] <= 20, "d20 roll should be between 1 and 20"
    assert result['total_attack'] == result['d20_roll'] + 5, "Total attack should be d20 roll plus attack bonus"
    assert 1 <= result['damage_roll'] <= 8, "Damage roll for 1d8 should be between 1 and 8"
    assert result['total_damage'] == result['damage_roll'], "Total damage should equal damage roll"

    # Test case 2: Different attack bonus and weapon damage
    result = simulate_attack_roll(3, "2d6")
    print("Test case 2 result:", result)
    assert 1 <= result['d20_roll'] <= 20, "d20 roll should be between 1 and 20"
    assert result['total_attack'] == result['d20_roll'] + 3, "Total attack should be d20 roll plus attack bonus"
    assert 2 <= result['damage_roll'] <= 12, "Damage roll for 2d6 should be between 2 and 12"
    assert result['total_damage'] == result['damage_roll'], "Total damage should equal damage roll"

    # Test case 3: Edge case with 0 attack bonus
    result = simulate_attack_roll(0, "1d4")
    print("Test case 3 result:", result)
    assert result['total_attack'] == result['d20_roll'], "Total attack should equal d20 roll when attack bonus is 0"
    assert 1 <= result['damage_roll'] <= 4, "Damage roll for 1d4 should be between 1 and 4"
    assert result['total_damage'] == result['damage_roll'], "Total damage should equal damage roll"

    print("All test cases passed!")

if __name__ == "__main__":
    test_simulate_attack_roll()