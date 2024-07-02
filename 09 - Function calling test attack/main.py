import random
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def simulate_attack_roll(attack_bonus, weapon_damage):
    d20_roll = random.randint(1, 20)
    total_attack = d20_roll + attack_bonus
    
    # Parse weapon damage (assuming format like "1d8")
    damage_dice, damage_sides = map(int, weapon_damage.split('d'))
    damage_roll = sum(random.randint(1, int(damage_sides)) for _ in range(int(damage_dice)))
    
    total_damage = damage_roll  # Remove attack bonus from total damage
    
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
                    "description": "The weapon damage dice (e.g., '1d8' for a longsword)."
                }
            },
            "required": ["attack_bonus", "weapon_damage"]
        }
    }
]

def process_tool_call(tool_name, tool_input):
    if tool_name == "attack_roll_simulator":
        return simulate_attack_roll(tool_input["attack_bonus"], tool_input["weapon_damage"])

def chat_with_claude(user_message):
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY not found in .env file")
        return None

    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    MODEL_NAME = "claude-3-opus-20240229"

    print(f"\n{'='*50}\nUser Message: {user_message}\n{'='*50}")

    try:
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=4096,
            messages=[{"role": "user", "content": user_message}],
            tools=tools,
        )

        print(f"\nInitial Response:")
        print(f"Stop Reason: {message.stop_reason}")
        print(f"Content: {message.content}")

        if message.stop_reason == "tool_calls":
            tool_call = message.content[-1]
            tool_name = tool_call.tool_calls[0].function.name
            tool_input = tool_call.tool_calls[0].function.arguments

            print(f"\nTool Used: {tool_name}")
            print(f"Tool Input: {tool_input}")

            tool_result = process_tool_call(tool_name, eval(tool_input))

            print(f"Tool Result: {tool_result}")

            response = client.messages.create(
                model=MODEL_NAME,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": message.content},
                    {"role": "tool", "content": str(tool_result)},
                ],
            )
        else:
            response = message

        final_response = response.content[0].text if response.content else "No response generated."
        print(f"\nFinal Response: {final_response}")

        return final_response

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    chat_with_claude("Simulate an attack roll for a longsword with +5 attack bonus.")