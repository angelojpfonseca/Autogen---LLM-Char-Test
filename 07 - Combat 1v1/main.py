import os
from dotenv import load_dotenv
from tool import attack_tool, damage_tool
import anthropic

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv('ANTHROPIC_API_KEY')

if not api_key:
    raise ValueError("No API key found. Please set the ANTHROPIC_API_KEY in your .env file.")

# Create the Anthropic client with the API key
client = anthropic.Anthropic(api_key=api_key)

system_prompt = """
# AI Dungeon Master: NPC Combat Simulator

You are an AI Dungeon Master tasked with simulating a round of combat between two NPCs in a fantasy role-playing game. Use the provided attack and damage tools to resolve combat mechanics while providing an engaging narrative description of the action.

## Your Responsibilities:
1. Interpret the user's input for NPC parameters.
2. Manage the combat round, determining initiative and action order.
3. Use the provided tools to resolve attacks and damage.
4. Provide a narrative description of the combat round.
5. Report the outcome and current state of both NPCs after the round.

## Input Format:
NPC1: Name, AC, HP, Attack Bonus, Weapon Damage
NPC2: Name, AC, HP, Attack Bonus, Weapon Damage

## Output Format:
1. Initiative Roll
2. First Attack (use attack tool)
3. Damage Resolution (use damage tool if hit)
4. Second Attack
5. Round Summary

Remember to use the provided tools for all rolls and calculations, and provide vivid descriptions of the combat.
"""


messages = [{"role": "user", "content": ""}]


       
response = client.messages.create(
system=system_prompt,
model="claude-3-sonnet-20240229",
messages=messages,
max_tokens=1000,
tool_choice={"type": "auto"},
tools=[attack_tool, damage_tool]
)
      
      
    