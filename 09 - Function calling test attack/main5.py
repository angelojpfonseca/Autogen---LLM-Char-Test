import random
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import ToolUseBlock

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def simulate_attack_roll(attack_bonus, weapon_damage):
    d20_roll = random.randint(1, 20)
    total_attack = d20_roll + attack_bonus
    
    # Parse weapon damage (assuming format like "2d6+3")
    damage_parts = weapon_damage.split('+')
    dice_part = damage_parts[0]
    bonus_part = int(damage_parts[1]) if len(damage_parts) > 1 else 0
    
    num_dice, dice_sides = map(int, dice_part.split('d'))
    damage_roll = sum(random.randint(1, dice_sides) for _ in range(num_dice))
    total_damage = damage_roll + bonus_part
    
    return {
        "d20_roll": d20_roll,
        "total_attack": total_attack,
        "damage_roll": damage_roll,
        "total_damage": total_damage
    }

# Define the tool
tools = [
    {
        "name": "attack_roll_simulator",
        "description": "Simulates a D&D 5e attack roll, including damage.",
        "input_schema": {
            "type": "object",
            "properties": {
                "attack_bonus": {
                    "type": "integer",
                    "description": "The attack bonus to add to the d20 roll."
                },
                "weapon_damage": {
                    "type": "string",
                    "description": "The weapon damage dice (e.g., '2d6+3' for a greatsword)."
                }
            },
            "required": ["attack_bonus", "weapon_damage"]
        }
    }
]

def process_tool_call(tool_name, tool_input):
    if tool_name == "attack_roll_simulator":
        return simulate_attack_roll(tool_input["attack_bonus"], tool_input["weapon_damage"])

from anthropic.types import ToolUseBlock

def chat_with_claude(messages):
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY not found in .env file")
        return None

    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    MODEL_NAME = "claude-3-opus-20240229"

    try:
        message = client.messages.create(
            model=MODEL_NAME,
            system="You have access to tools, but only use them when necessary. If a tool is not required, respond as normal. When you decide to use a tool, always provide the exact input for the tool in your response.",
            max_tokens=4096,
            messages=messages,
            tools=tools,
        )

        print(f"Initial response: {message.content}")

        # Check if the message content indicates tool use
        tool_use_block = next((content for content in message.content if isinstance(content, ToolUseBlock)), None)

        if tool_use_block:
            tool_name = tool_use_block.name
            tool_input = tool_use_block.input

            print(f"Tool Used: {tool_name}")
            print(f"Tool Input: {tool_input}")

            # Call the tool
            tool_result = process_tool_call(tool_name, tool_input)
            print(f"Tool Result: {tool_result}")

            # Create a new message with the tool result incorporated into the assistant's response
            tool_result_message = f"Based on the attack roll simulation, here are the results: {tool_result}"
            response = client.messages.create(
                model=MODEL_NAME,
                max_tokens=4096,
                messages=messages + [
                    {"role": "assistant", "content": tool_result_message},
                ],
            )
            return response.content[0].text if response.content else "No response generated."
        else:
            return message.content[0].text if message.content else "No response generated."

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    conversation = []
    print("Welcome to the D&D 5e Attack Roll Simulator Chatbot!")
    print("You can ask about simulating attack rolls or discuss D&D topics.")
    print("Type 'exit' to end the conversation.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Thank you for using the D&D 5e Attack Roll Simulator Chatbot. Goodbye!")
            break

        conversation.append({"role": "user", "content": user_input})
        response = chat_with_claude(conversation)

        if response:
            print(f"\nClaude: {response}")
            conversation.append({"role": "assistant", "content": response})
        else:
            print("\nClaude: I'm sorry, I encountered an error. Please try again.")
            # Remove the last user message if there was an error
            conversation.pop()
            
if __name__ == "__main__":
    main()