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

def get_claude_decision(player: str, game_state: str, opponent: str) -> tuple:
    """
    Get a decision and small talk from Claude for the next move.
    
    Args:
    player (str): The player making the decision
    game_state (str): The current state of the game
    opponent (str): The name of the opponent
    
    Returns:
    tuple: (move, small_talk)
    """
    prompt = f'''{anthropic.HUMAN_PROMPT} You are an AI playing Jo Ken Po (Rock Paper Scissors). Your goal is to win the game. You are {player}. The current game state is: {game_state}. Your opponent is {opponent}.

Please respond by calling the following functions:

make_small_talk(text: str)
make_move(move: str)

For example:
make_small_talk("Hey there! Ready for another round?")
make_move("rock")

{anthropic.AI_PROMPT}'''

    response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-2",
        max_tokens_to_sample=300
    )

    # Print raw response for debugging
    print(f"Raw response from Claude:\n{response.completion}\n")

    # Extract the small talk and move from Claude's response
    response_text = response.completion.strip()
    small_talk_match = re.search(r'make_small_talk\("(.*)"\)', response_text)
    move_match = re.search(r'make_move\("(\w+)"\)', response_text)
    
    small_talk = small_talk_match.group(1) if small_talk_match else "No small talk this time."
    move = move_match.group(1).lower() if move_match else random.choice(['rock', 'paper', 'scissors'])
    
    # Print extracted information for debugging
    print(f"Extracted small talk: {small_talk}")
    print(f"Extracted move: {move}\n")
    
    return move, small_talk

def main():
    player1_score = 0
    player2_score = 0
    rounds_played = 0

    while max(player1_score, player2_score) < 2 and rounds_played < 3:
        rounds_played += 1
        print(f"\n--- Round {rounds_played} ---")
        
        game_state = get_game_state(player1_score, player2_score, rounds_played)
        
        # Get moves and small talk from Claude agents
        move1, small_talk1 = get_claude_decision("Player 1", game_state, "Player 2")
        move2, small_talk2 = get_claude_decision("Player 2", game_state, "Player 1")
        
        print(f"Player 1: {small_talk1}")
        print(f"Player 2: {small_talk2}")
        
        result = play_jo_ken_po(move1, move2)
        
        print(f"\nPlayer 1 played {move1}")
        print(f"Player 2 played {move2}")
        print(f"Result: {result}")
        
        if result == "Player 1 wins":
            player1_score += 1
        elif result == "Player 2 wins":
            player2_score += 1
        
        print(f"\nCurrent score - Player 1: {player1_score}, Player 2: {player2_score}")

    winner = "Player 1" if player1_score > player2_score else "Player 2"
    print(f"\nGame over! {winner} wins!")

if __name__ == "__main__":
    main()