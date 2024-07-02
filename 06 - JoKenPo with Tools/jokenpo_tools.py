from pydantic import BaseModel
from typing import Literal

class JoKenPoInput(BaseModel):
    move1: Literal["rock", "paper", "scissors"]
    move2: Literal["rock", "paper", "scissors"]

class GameStateInput(BaseModel):
    player1_score: int
    player2_score: int
    rounds_played: int

tools = [
    {
        "name": "play_jo_ken_po",
        "description": "Play a round of Jo Ken Po (Rock Paper Scissors)",
        "input_schema": {
            "type": "object",
            "properties": {
                "move1": {"type": "string", "enum": ["rock", "paper", "scissors"]},
                "move2": {"type": "string", "enum": ["rock", "paper", "scissors"]}
            },
            "required": ["move1", "move2"]
        }
    },
    {
        "name": "get_game_state",
        "description": "Get the current game state",
        "input_schema": {
            "type": "object",
            "properties": {
                "player1_score": {"type": "integer"},
                "player2_score": {"type": "integer"},
                "rounds_played": {"type": "integer"}
            },
            "required": ["player1_score", "player2_score", "rounds_played"]
        }
    }
]

def play_jo_ken_po(move1: str, move2: str) -> str:
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
    return f"Player 1 score: {player1_score}, Player 2 score: {player2_score}, Rounds played: {rounds_played}"

def process_tool_call(tool_name, tool_input):
    if tool_name == "play_jo_ken_po":
        validated_input = JoKenPoInput(**tool_input)
        result = play_jo_ken_po(validated_input.move1, validated_input.move2)
        return {"result": result}
    elif tool_name == "get_game_state":
        validated_input = GameStateInput(**tool_input)
        result = get_game_state(validated_input.player1_score, validated_input.player2_score, validated_input.rounds_played)
        return {"state": result}

# Explicitly export the tools and process_tool_call
__all__ = ['tools', 'process_tool_call']