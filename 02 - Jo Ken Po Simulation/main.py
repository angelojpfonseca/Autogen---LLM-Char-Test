import os
from dotenv import load_dotenv
import anthropic
import re
import random
from game_functions import play_jo_ken_po, get_game_state

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv('ANTHROPIC_API_KEY')

if not api_key:
    raise ValueError("No API key found. Please set the ANTHROPIC_API_KEY in your .env file.")

# Create the Anthropic client with the API key
client = anthropic.Anthropic(api_key=api_key)

def get_claude_decision(player: str, game_state: str) -> str:
    """
    Get a decision from Claude for the next move.
    
    Args:
    player (str): The player making the decision
    game_state (str): The current state of the game
    
    Returns:
    str: The decided move
    """
    prompt = f"""Human: You are an AI playing Jo Ken Po (Rock Paper Scissors). Your goal is to win the game.
You are {player}. The current game state is: {game_state}. What's your next move?

Please respond in the following format:
make_move(move="your_move")

Where "your_move" is either "rock", "paper", or "scissors".

Assistant: Based on the current game state, I'll make my move for this round of Jo Ken Po. Here's my decision:

make_move(move="
Human: ")"""

    response = client.completions.create(
        prompt=prompt,
        stop_sequences=['"'],
        model="claude-v1",
        max_tokens_to_sample=300
    )

    # Extract the move from Claude's response
    move_match = re.search(r'make_move\(move="(\w+)"\)', response.completion)
    if move_match:
        return move_match.group(1)
    else:
        # If we can't parse the move, default to a random move
        return random.choice(['rock', 'paper', 'scissors'])

def main():
    player1_score = 0
    player2_score = 0
    rounds_played = 0

    while max(player1_score, player2_score) < 2 and rounds_played < 5:
        rounds_played += 1
        print(f"\nRound {rounds_played}:")
        
        game_state = get_game_state(player1_score, player2_score, rounds_played)
        
        # Get moves from Claude agents
        move1 = get_claude_decision("Player 1", game_state)
        move2 = get_claude_decision("Player 2", game_state)
        
        result = play_jo_ken_po(move1, move2)
        
        print(f"Player 1 played {move1}, Player 2 played {move2}")
        print(f"Result: {result}")
        
        if result == "Player 1 wins":
            player1_score += 1
        elif result == "Player 2 wins":
            player2_score += 1
        
        print(f"Current score - Player 1: {player1_score}, Player 2: {player2_score}")

    winner = "Player 1" if player1_score > player2_score else "Player 2"
    print(f"\nGame over! {winner} wins!")

if __name__ == "__main__":
    main()