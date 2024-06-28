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

First, make a brief small talk comment to your opponent (1-2 sentences). Then, make your move.

Please respond in the following format:
Small talk: [Your small talk here]
Move: [Your move here (rock, paper, or scissors)]

{anthropic.AI_PROMPT} Certainly! I'll engage in some small talk and then make my move. Here's my response:

Small talk: Hey {opponent}! This game is getting intense, isn't it? I'm really enjoying our match so far.

Move: rock

{anthropic.HUMAN_PROMPT} Great! Now it's your turn to play. Remember to change your strategy and small talk each time. What's your next move and small talk?

{anthropic.AI_PROMPT} Absolutely! I'll change things up for this round. Here's my new response:

Small talk: You know, {opponent}, I've been analyzing our previous moves, and I must say, you're quite the formidable opponent! Let's see how this round goes.

Move: paper

{anthropic.HUMAN_PROMPT} Excellent! Now, provide one more unique small talk and move combination.

{anthropic.AI_PROMPT} Certainly! I'll give you another unique combination. Here it is:

Small talk: {opponent}, did you know that some cultures have their own versions of Rock Paper Scissors? In Japan, they sometimes use "Jan-Ken-Pon!" Maybe we should try that next time for fun!

Move: scissors

{anthropic.HUMAN_PROMPT} Perfect! Now, based on the current game state, provide a final small talk and move combination that fits the situation.

{anthropic.AI_PROMPT}'''

    response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-2",
        max_tokens_to_sample=300
    )

    # Extract the small talk and move from Claude's response
    response_text = response.completion.strip()
    small_talk_match = re.search(r'Small talk: (.*)', response_text, re.IGNORECASE)
    move_match = re.search(r'Move: (\w+)', response_text, re.IGNORECASE)
    
    small_talk = small_talk_match.group(1) if small_talk_match else "No small talk this time."
    move = move_match.group(1).lower() if move_match else random.choice(['rock', 'paper', 'scissors'])
    
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