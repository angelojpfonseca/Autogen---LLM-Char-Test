import random

def play_jo_ken_po(move1: str, move2: str) -> str:
    """
    Play a round of Jo Ken Po (Rock Paper Scissors).
    
    Args:
    move1 (str): Move of the first player
    move2 (str): Move of the second player
    
    Returns:
    str: Result of the game
    """
    moves = ['rock', 'paper', 'scissors']
    if move1 not in moves or move2 not in moves:
        raise ValueError("Invalid move. Must be 'rock', 'paper', or 'scissors'.")
    
    if move1 == move2:
        return "Draw"
    elif (
        (move1 == 'rock' and move2 == 'scissors') or
        (move1 == 'scissors' and move2 == 'paper') or
        (move1 == 'paper' and move2 == 'rock')
    ):
        return "Player 1 wins"
    else:
        return "Player 2 wins"

def get_game_state(player1_score: int, player2_score: int, rounds_played: int) -> str:
    """
    Get the current game state.
    
    Args:
    player1_score (int): Score of player 1
    player2_score (int): Score of player 2
    rounds_played (int): Number of rounds played
    
    Returns:
    str: Current game state
    """
    return f"Player 1 score: {player1_score}, Player 2 score: {player2_score}, Rounds played: {rounds_played}"